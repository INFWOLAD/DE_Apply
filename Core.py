import configparser
import json
import os
import sys
from datetime import datetime

import requests
import urllib3

from Get_Position import main as get_position
from Position_Apply import main as position_apply


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
    print(config_path)
    conf = configparser.RawConfigParser()
    conf.read(config_path)
    wecom = conf.items('Wecom')
    user = conf.items('User')
    other = conf.items('Other')
    return wecom, user, other


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    wecom_config, user_config, other_config = get_config()
    item_num, uuid = list(zip(*other_config))[1]
    print('📹监控程序启动中...')
    Get_status = False
    position_date = ''
    while len(position_date) == 0:
        Get_status, position_date, first_content, second_content = get_position(item_num)
        print(str(datetime.now())[0:19] + '>>>✔️仍然无可预约名额')
    wecom_cid, wecom_aid, wecom_secret, wecom_touid = list(zip(*wecom_config))[1]
    if Get_status is not True:
        print('⚠️多次获取位置信息失败，已退出')
        send_to_wecom('⚠️多次获取位置信息失败，已退出', wecom_cid, wecom_aid, wecom_secret, wecom_touid)
        sys.exit()
    else:
        print('📖正在尝试预约...')
        first_name, last_name, email, birthday, street, zipcode, city, phone, gender = list(zip(*user_config))[1]
        position_status, appointment_info = position_apply(position_date, first_content, second_content, first_name, last_name, email, birthday, street, zipcode, city, phone, gender, uuid)
    if position_status:
        outcome = '📤已完成预约>>相关信息如下：\nBuchungsreferenz：' + appointment_info['AdditionalInformation']
        print(outcome)
        send_to_wecom(outcome, wecom_cid, wecom_aid, wecom_secret, wecom_touid)
    else:
        print('❌尝试预约但预约失败，请手动尝试！')
        send_to_wecom('✅发现预约位置，请手动预约！', wecom_cid, wecom_aid, wecom_secret, wecom_touid)