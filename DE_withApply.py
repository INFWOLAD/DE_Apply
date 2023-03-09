"""
    2023-3-8 22:36 Start analysis
    2023-3-9 23:49 Start programming
    2023-3-9 01:23 Finish Core
    2023-3-9 15:39 Start adding applications
    2023-3-9 16:06 Finish adding
    2023-3-9 18:08 Fixed some bugs
    This program is just for the person who needs to solve their own problems.
    Please do not use this program for others.
    There may be some errors using this program because of my fucking abilities.
"""
import configparser
import json
import os
import time
from datetime import datetime

import requests
import urllib3


# This function can be replaced by email send-robots.
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


# Read the information from config.ini (convenient for others).
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


# This is the first request getting every section's content on the first page.
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
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                              "like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
                "Referer": "https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued",
                "Accept-Language": "en-GB,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.json()))
        return response.json()[int(item_num)]
        # Getting No.15 item is the normal function of it.

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Getting some items' values is the function of it.
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
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
                "webid": "qtermin-stadt-duisburg-abh-sued",
                "Host": "www.qtermin.de",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.json()))
        return response.json()[0]
        # [{}] >> {}

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# By getting the information via the first request, now this function tries to know if there is a position to apply.
def end_get(date, sid, duration, appfuture, appdeadline, appdeadlinewm, msdcm):
    try:
        response = requests.get(
            url="https://www.qtermin.de/api/timeslots",
            # If some params is lost, you can modify it by crossing params.
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
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
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
    #     Here just one list.
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Outstanding module to operate all requests of getting positions' number.
def get_set():
    try:
        first_content = first_request()
        # print(first_content)
        ymd = time.strftime('%Y-%m-%d', time.localtime())
        second_content = second_request()
        # If the parameters isn't permanent, need to add things here.
        end_content = end_get(ymd, first_content['sid'], first_content['duration'], second_content['appfuture'],
                              second_content['appdeadline'], second_content['appdeadlinewm'], second_content['msdcm'])
        print(end_content)
    except:
        send_to_wecom("⚠️德国注册监控出错！", wecom_cid, wecom_aid, wecom_secret, wecom_touid)
        return False, 'error', 'error', 'error'
    else:
        return True, end_content, first_content, second_content


# Only run when there is a position. It can operate every date.
def get_date_detail(date, sid, duration, appfuture, appdeadline, msdcm, appdeadlinewm):
    try:
        response = requests.get(
            url="https://www.qtermin.de/api/timeslots",
            params={
                "date": date,
                "serviceid": sid,
                "capacity": "1",
                "caching": "false",
                "duration": duration,
                "cluster": "false",
                "slottype": "0",
                "fillcalendarstrategy": "0",
                "showavcap": "false",
                "appfuture": appfuture,
                "appdeadline": appdeadline,
                "msdcm": msdcm,
                "oneoff": "null",
                "appdeadlinewm": appdeadlinewm,
                "tz": "W. Europe Standard Time",
                "tzaccount": "W. Europe Standard Time",
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
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "webid": "qtermin-stadt-duisburg-abh-sued",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Get the location of the date we chose.(No.1 normally)
def get_location(calendarid):
    try:
        response = requests.get(
            url="https://www.qtermin.de/api/calendar",
            params={
                "calendarid": calendarid,
                "companydataonly": "1",
            },
            headers={
                "Accept": "application/json, text/plain",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Host": "www.qtermin.de",
                "Referer": "https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "webid": "qtermin-stadt-duisburg-abh-sued",
            },
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# This function will apply for you by using the information in the configuration.
def submit_app(sid, servicetext, inclsg_text, first_name, last_name, email, birthday, street, zipcode, city, phone,
               gender, calendarname, start, end, calendarid, back_street, uuid, servicescapacity,
               servicescapacitydetails):
    submit_data = f'language=de&bookingtype=Internet&bookingurl=https%3A%2F%2Fwww.qtermin.de%2Fqtermin-stadt-duisburg' \
                  f'-abh-sued&agbaccepted=false&dataprivacyaccepted=true&feedbackpermissionaccepted=false&newsletter' \
                  f'=false&services={sid}&servicestext={servicetext}&servicesinclsgtext={inclsg_text}&FirstName=' \
                  f'{first_name}&LastName={last_name}&Email={email}&Birthday={birthday}&Street={street}&ZIP=' \
                  f'{zipcode}&City={city}&Phone={phone}&Salutation={gender}&Notes=&bookerinfo=Anrede%09' \
                  f'{gender}%0D%0AVorname%09{first_name}%0D%0AName%09{last_name}%0D%0AStrasse%09{street}%0D%0APLZ%09' \
                  f'{zipcode}%0D%0AOrt%09{city}%0D%0ATelefon%09{phone}%0D%0AE-Mail%09{email}%0D%0AGeburtsdatum%09' \
                  f'{birthday}%0D%0A%09%0D%0ATerminerinnerung%0912%20Stunden%20vor%20Termin%0D%0A&calendarname=' \
                  f'{calendarname}&start={start}&end={end}&calendarid={calendarid}&calname={calendarname}&location=' \
                  f'{back_street}&tzaccount=W. Europe Standard Time&checkexist=1&pricegross=0&appgroup=' \
                  f'{uuid}&capacity=1&servicescapacity={servicescapacity}&servicescapacitydetails=' \
                  f'{servicescapacitydetails}&canceldeadline=0&sync=1&sendemail=1&appointmentreminderhours=-12' \
                  f'&appointmentreminderhours2=-4&confirmappointment=1&confirmtime=120&sendinvoice=1&nrappbooked=1' \
                  f'&capused=false&capmaxused=30&customerconfirm=true&calselid=-1&lnm=1&emailm=1&storeip=false&apw' \
                  f'=false '
    try:
        response = requests.post(
            url="https://www.qtermin.de/api/appointment",
            headers={
                "Host": "www.qtermin.de",
                "Connection": "keep-alive",
                "Content-Length": "1760",
                "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
                "Accept": "application/json, text/plain",
                "Content-Type": "application/json",
                "sec-ch-ua-mobile": "?0",
                "webid": "qtermin-stadt-duisburg-abh-sued",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
                "sec-ch-ua-platform": "\"macOS\"",
                "Origin": "https://www.qtermin.de",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.qtermin.de/qtermin-stadt-duisburg-abh-sued",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            },
            data=submit_data
        )
        # print('Response HTTP Status Code: {status_code}'.format(
        #     status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


# Because of the complex steps of submitting, we use an outstanding model here.
def apply(retry_time):
    try:
        first_name, last_name, email, birthday, street, zipcode, city, phone, gender = list(zip(*user_config))[1]
        appoint_date = get_date_detail(end_content[0]['start'][0:10], first_content['sid'],
                                       first_content['duration'], second_content['appfuture'],
                                       second_content['appdeadline'], second_content['msdcm'],
                                       second_content['appdeadlinewm'])
        # print(appoint_date)
        location_data = get_location(appoint_date[0]['calendarid'])
        appoint_end = submit_app(first_content['sid'], first_content['s'] + " (1)",
                                 first_content['sg'] + '<br>' + first_content['s'] + " (1)", first_name,
                                 last_name,
                                 email, birthday, street, zipcode, city, phone, gender,
                                 appoint_date[0]['calendarname'], appoint_date[0]['start'],
                                 appoint_date[0]['end'],
                                 appoint_date[0]['calendarid'], location_data[0]['street'], uuid,
                                 {first_content['sid']: "1"}, first_content['s'] + '%091%0D%0A')
        # print(appoint_end)
        # print(appoint_end['StatusMsg'])
        if appoint_end['StatusMsg'] == 'Appointment created successfully!':
            outcome = '📤已完成预约>>相关信息如下：\nBuchungsreferenz：' + appoint_end['AdditionalInformation']
            print(outcome)
            send_to_wecom(outcome, wecom_cid, wecom_aid, wecom_secret, wecom_touid)
            return False, retry_time
        else:
            print('❌尝试预约但预约失败，重试中')
            retry_time += 1
            return True, retry_time
    except:
        print('预约存在问题')
        retry_time += 1
        return True, retry_time
    #     Retry applying.


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    wecom_config, user_config, other_config = get_config()
    # Using zip to get the second parameter isn't recommend way! But I like it.
    wecom_cid, wecom_aid, wecom_secret, wecom_touid = list(zip(*wecom_config))[1]
    item_num, uuid = list(zip(*other_config))[1]
    active_num = True
    retry_apply = False
    retry_time = 0
    print('📹预约监控已启动')
    send_to_wecom('📹预约监控已启动', wecom_cid, wecom_aid, wecom_secret, wecom_touid)
    while (active_num or retry_apply) and retry_time < 2:
        # print('在循环中...')
        now_time = datetime.now()
        # if now_time.minute == 0:
        #     send_to_wecom("仍在监控中", wecom_cid, wecom_aid, wecom_secret, wecom_touid)
        err_info, end_content, first_content, second_content = get_set()
        if len(end_content) != 0 and err_info:
            msg = '✅存在名额，正在自动预约！详细日期如下：'
            # print(msg)
            # Loop to get all dates.
            for i in end_content:
                msg = msg + '\n' + i['start'][0:10]
            print(msg)
            # send_to_wecom(msg, wecom_cid, wecom_aid, wecom_secret, wecom_touid)
            send_to_wecom(msg, wecom_cid, wecom_aid, wecom_secret, wecom_touid)
            print('🛠正在尝试预约...')
            retry_apply = apply(retry_time)
            # If there are something wrong, try to resend.
            active_num = False
        elif err_info:
            print(str(now_time)[0:19] + '>>>✔️仍然无可预约名额')
            retry_apply = False
        else:
            # print('正在退出循环！')
            active_num = False
            retry_apply = False
    if retry_time > 1:
        send_to_wecom('🔔尝试预约但预约失败，请手动预约', wecom_cid, wecom_aid, wecom_secret, wecom_touid)
    print("💤程序已停止，请手动重启！")
    send_to_wecom("💤程序已停止，请手动重启！", wecom_cid, wecom_aid, wecom_secret, wecom_touid)
