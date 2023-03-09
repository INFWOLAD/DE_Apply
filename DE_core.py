"""
    2023-3-8 22:36
    This program is just for the person who needs to solve their own problems.
    Please do not use this program for others.
    There may be some errors using this program because of my fucking abilities.
"""
import json
import time
from datetime import datetime
import urllib3
import requests


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


def first_request():
    try:
        response = requests.get(
            url="https://www.qtermin.de/api/servicegroupservice",
            params={
                "cache": "1",
                "w": "qtermin-stadt-duisburg-abh-sued",
                "v": "413",
                "lang": "de",
            },
            headers={
                "Host": "www.qtermin.de",
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "webid": "qtermin-stadt-duisburg-abh-sued",
                "Accept": "application/json, text/plain",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
                "Referer": "https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued",
                "Accept-Language": "en-GB,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.json()))
        return response.json()[16]
        # return response.json()[1]

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def second_request():
    try:
        response = requests.get(
            url="https://www.qtermin.de/api/settingbs",
            params={
                "t": "",
            },
            headers={
                "accept": "application/json, text/plain",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "content-type": "application/json",
                "pragma": "no-cache",
                "referer": "https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
                "webid": "qtermin-stadt-duisburg-abh-sued",
                "Host": "www.qtermin.de",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.json()))
        return response.json()[0]
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def end_get(date, sid, duration, appfuture, appdeadline, appdeadlinewm, msdcm):
    try:
        response = requests.get(
            url="https://www.qtermin.de/api/timeslots",
            params={
                "date": date,
                "serviceid": sid,
                "rangesearch": "1",
                "caching": "false",
                "capacity": "1",
                "duration": duration,
                "cluster": "false",
                "slottype": "0",
                "fillcalendarstrategy": "0",
                "showavcap": "false",
                "appfuture": appfuture,
                "appdeadline": appdeadline,
                "appdeadlinewm": appdeadlinewm,
                "oneoff": "null",
                "msdcm": msdcm,
                "calendarid": "",
            },
            headers={
                "Accept": "application/json, text/plain",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Host": "www.qtermin.de",
                "Pragma": "no-cache",
                "Referer": "https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "webid": "qtermin-stadt-duisburg-abh-sued",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.json()))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def get_set():
    try:
        first_content = first_request()
        # print(first_content)
        ymd = time.strftime('%Y-%m-%d', time.localtime())
        second_content = second_request()
        # If the parameters isn't permanent, need to add things here.
        end_content = end_get(ymd, first_content['sid'], first_content['duration'], second_content['appfuture'],
                              second_content['appdeadline'], second_content['appdeadlinewm'], second_content['msdcm'])
        # print(end_content)
    except:
        send_to_wecom("⚠️德国注册监控出错！", "wwc6056f422446a669", "1000004",
                      "DMvzOCRzLprvG5o4PndkiTH3qH8xzzYAziNevPEAzzk",
                      "@all")
        return False, 'error'
    else:
        return True, end_content


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    active_num = True
    while active_num:
        err_info, end_content = get_set()
        if len(end_content) != 0 and err_info:
            msg = '✅可预约！详细日期如下：\n'
            for i in end_content:
                msg += i['start'][0:10] + '\n'
            # print(msg)
            send_to_wecom(msg, "wwc6056f422446a669", "1000003",
                          "MApFuF3lgIiy8mwnygFFWJuEQRICnfvnhO7S1PqiYd0",
                          "BuXiangQiChuang")
            send_to_wecom(msg, "wwc6056f422446a669", "1000004",
                          "DMvzOCRzLprvG5o4PndkiTH3qH8xzzYAziNevPEAzzk",
                          "@all")
            active_num = False
        elif err_info:
            print(str(datetime.now())[0:16] + '>>>✔️仍然无可预约名额')
        else:
            print("❌错误！请及时检查！")
            active_num = False
