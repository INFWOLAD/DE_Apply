import configparser
import json
import os
import random
import sys
import threading
import time
from datetime import datetime

import requests
import urllib3

import Get_Position
import Position_Apply


def send_to_wecom(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def get_config():
    pre_dir = os.path.split(os.path.realpath(__file__))[0]
    config_path = os.path.join(pre_dir, 'config.ini')
    # print(config_path)
    conf = configparser.RawConfigParser()
    conf.read(config_path)
    wecom = conf.items('WecomItem')
    user = conf.items('User')
    return wecom, user


def replacer(n):
    t = int(random.random() * 16)
    i = t if n == 'x' else (t & 3) | 8
    return hex(i)[2:]


def if_position(is_test=0):
    global Get_status, position_date
    try_again = 0
    interval_time = 0
    while try_again < 5 and position_date == [] and time.strftime('%H:%M', time.localtime()) != '20:26':
        # lock.acquire()
        # print(position_date)
        Get_status, position_date = Get_Position.main(first_response, second_response)
        # lock.release()
        if position_date == 0:
            try_again += 1
            time.sleep(5)
        elif is_test == 3:
            interval_time = int(str(datetime.now())[17:19]) - interval_time
            # print(interval_time)
            try_again += is_test
        else:
            try_again = 0
            print(str(datetime.now())[0:22] + '>>>🔘仍然无可预约名额')
            # time_now += 1
    return interval_time


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print(str(datetime.now())[0:19] + '>>>📷监控程序启动中...')

    wecom_config, user_config = get_config()
    wecom_on, wecom_cid, wecom_aid, wecom_secret, wecom_touid, item_num, close_multi = list(zip(*wecom_config))[1]
    first_name, last_name, email, birthday, street, zipcode, city, phone, gender = list(zip(*user_config))[1]
    uuid = ''.join([replacer(c) if c in 'xy' else c for c in 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'])

    retry_count = 0
    while retry_count < 2:
        get_fs_status, first_response, second_response = Get_Position.get_fs(item_num)
        if get_fs_status is not True:
            retry_count += 1
            time.sleep(10)
        else:
            break

    Get_status = False
    position_date = []
    threads = []
    # time_now = 0
    print(str(datetime.now())[0:19] + '>>>📡正在评估所需并发数...')
    interval = int(if_position(3))
    multi_open = ''
    if close_multi:
        interval_seconds = 1
        multi_open = '您设置了稳定模式，'
    elif interval <= 0:
        interval_seconds = 1
    elif interval >= 3:
        interval_seconds = 3
    else:
        interval_seconds = interval
    print(str(datetime.now())[0:19] + f'>>>📡{multi_open}并发数将设置为{interval_seconds}...')

    # lock = threading.Lock()
    print(str(datetime.now())[0:19] + '>>>📸启动成功，Ver Mar.21')

    for i in range(int(interval_seconds)):
        t = threading.Thread(target=if_position, daemon=True)
        threads.append(t)
        t.start()
        time.sleep(1)
    for t in threads:
        t.join()
    if Get_status is not True:
        print(str(datetime.now())[0:19] + '>>>⚠️网络连接失败，已退出')
        send_to_wecom('⚠️网络连接失败，已退出', wecom_cid, wecom_aid, wecom_secret, 'YanGen') if wecom_on else None
        sys.exit()
    elif position_date:
        print(str(datetime.now())[0:19] + '>>>📖正在尝试预约...')
        send_to_wecom('✅发现预约位置，正在自动预约...', wecom_cid, wecom_aid, wecom_secret, wecom_touid)
        position_status, appointment_info = Position_Apply.main(position_date, first_response, second_response,
                                                                first_name, last_name, email, birthday, street, zipcode,
                                                                city, phone, gender, uuid)
        outcome = '📤已完成预约\n相关信息如下：\nBuchungsreferenz：' + appointment_info[
            'AdditionalInformation'] if position_status else '❌尝试预约但预约失败，请手动尝试！'
        print(str(datetime.now())[0:19] + '>>>' + outcome)
        send_to_wecom(outcome, wecom_cid, wecom_aid, wecom_secret, wecom_touid) if wecom_on else None
    else:
        print(str(datetime.now())[0:22] + '>>>💤程序进入重启时间')
