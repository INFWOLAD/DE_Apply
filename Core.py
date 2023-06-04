import configparser
import json
import os
import random
import sys
import time
from datetime import datetime

import requests
import urllib3


class Position:
    def __init__(self, user):
        self.user = user
        self.expect_date_start = user.expect_date_start
        self.expect_date_end = user.expect_date_end
        self.first_response, self.second_response = self.get_fs()
        self.position_date = []
        self.can_apply = False

    @staticmethod
    def get_request(url, params, headers):
        try:
            response = requests.get(url=url, params=params, headers=headers, verify=False, timeout=4)
            status_code = response.status_code
            return response, status_code
        except:
            print('⚠️HTTP Request failed，正在重试')
            return None, 999

    def get_fs(self):
        first_response, first_status = self.get_request(
            "https://www.qtermin.de/api/servicegroupservice",
            {
                "cache": "1",
                "w": "qtermin-stadt-duisburg-abh-sued",
                "v": "413",
                "lang": "de",
            }, {
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
            })
        second_response, second_status = self.get_request(
            "https://www.qtermin.de/api/settingbs",
            {
                "t": "",
            }, {
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
            })
        if first_status + second_status != 400:
            time.sleep(10)
            first_response, second_response = self.get_fs()
        else:
            print(
                str(datetime.now())[0:19] + '>>>🗓您所要预定的是:\n\n' + first_response.json()[int(self.user.item_num)][
                    's'] + '\n')
            print(str(datetime.now())[0:19] + f'>>>📝你所期望的日期为{self.expect_date_start}至{self.expect_date_end}')
            first_response, second_response = first_response.json()[int(self.user.item_num)], second_response.json()[0]
        return first_response, second_response

    def get_position(self, first_content, second_content):
        # print(first_content)
        # print(second_content)
        end_content, end_status = self.get_request(
            "https://www.qtermin.de/api/timeslots",
            {
                "date": time.strftime('%Y-%m-%d', time.localtime()),
                "serviceid": first_content['sid'],
                "rangesearch": "1",
                "caching": "false",
                "capacity": "1",
                "duration": first_content['duration'],
                "cluster": "false",
                "slottype": "0",
                "fillcalendarstrategy": "0",
                "showavcap": "false",
                "appfuture": second_content['appfuture'],
                "appdeadline": second_content['appdeadline'],
                "appdeadlinewm": second_content['appdeadlinewm'],
                "oneoff": "null",
                "msdcm": second_content['msdcm'],
                "calendarid": "",
            }, {
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
            })
        return end_content, end_status

    def if_position(self):
        try_again = 0
        while try_again < 5 and self.position_date == []:
            # lock.acquire()
            # print(position_date)
            try:
                position_data, end_status = self.get_position(self.first_response, self.second_response)
            except:
                end_status = 0
            if end_status != 200:
                print('⚠️网络原因导致获取信息失败，尝试修复中')
                try_again += 1
                time.sleep(5)
                continue
            else:
                try_again = 0
                self.position_date = position_data.json()
                print(str(datetime.now())[0:22] + '>>>🔘仍然无可预约名额')
                # time_now += 1
        if try_again > 4:
            print(str(datetime.now())[0:19] + '>>>⚠️网络连接失败，已退出')
            self.user.send_to_wecom('⚠️网络连接失败，已退出') if self.user.wecom_on else None
            sys.exit()
        else:
            self.check_date()

    def check_date(self):
        start_date_stamp = round(time.mktime(time.strptime(self.expect_date_start + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
        end_date_stamp = round(time.mktime(time.strptime(self.expect_date_end + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
        # print(position_date)
        pop_items = []
        for i in range(len(self.position_date)):
            exist_date_stamp = round(
                time.mktime(time.strptime(self.position_date[i]['start'][0:10] + ' 00:00:00', "%Y-%m-%d %H:%M:%S")))
            print(str(datetime.now())[0:19] + '>>>📖位置时间戳：' + str(exist_date_stamp))
            if not (start_date_stamp <= exist_date_stamp <= end_date_stamp):
                pop_items.append(i)
        pop_items.reverse()
        for j in pop_items:
            self.position_date.pop(int(j))
        # print(position_date)
        if len(self.position_date) == 0:
            print(str(datetime.now())[0:19] + '>>>📖存在空位但不在预期时间...')
            self.can_apply = False
        else:
            self.can_apply = True


class Apply:
    def __init__(self, position, user):
        self.position = position
        self.user = user

    @staticmethod
    def get_request(url, params, headers):
        try:
            response = requests.get(url=url, params=params, headers=headers, verify=False, timeout=4)
            status_code = response.status_code
            return response.json(), status_code
        except:
            print('HTTP Request failed')
            return None, 999

    @staticmethod
    def post_request(url, headers, data):
        try:
            response = requests.post(url=url, headers=headers, data=data, verify=False)
            status_code = response.status_code
            return response.json(), status_code
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
            return None, 999

    def apply(self):
        appoint_date, data_status = self.get_request(
            "https://www.qtermin.de/api/timeslots",
            {
                "date": self.position.position_date[0]['start'][0:10],
                "serviceid": self.position.first_response['sid'],
                "capacity": "1",
                "caching": "false",
                "duration": self.position.first_response['duration'],
                "cluster": "false",
                "slottype": "0",
                "fillcalendarstrategy": "0",
                "showavcap": "false",
                "appfuture": self.position.second_response['appfuture'],
                "appdeadline": self.position.second_response['appdeadline'],
                "msdcm": self.position.second_response['msdcm'],
                "oneoff": "null",
                "appdeadlinewm": self.position.second_response['appdeadlinewm'],
                "tz": "W. Europe Standard Time",
                "tzaccount": "W. Europe Standard Time",
                "calendarid": "",
            }, {
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
        location_info, location_status = self.get_request(
            "https://www.qtermin.de/api/calendar",
            {
                "calendarid": appoint_date[0]['calendarid'],
                "companydataonly": "1",
            }, {
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
        if data_status + location_status == 400:
            sid = self.position.first_response['sid']
            servicetext = self.position.first_response['s'] + " (1)"
            inclsg_text = self.position.first_response['sg'] + '<br>' + self.position.first_response['s'] + " (1)"
            calendarname, start, end, calendarid, back_street = appoint_date[0]['calendarname'], appoint_date[0][
                'start'], \
                                                                appoint_date[0]['end'], appoint_date[0]['calendarid'], \
                                                                location_info[0]['street']
            servicescapacity, servicescapacitydetails = {self.position.first_response['sid']: "1"}, \
                                                        self.position.first_response['s'] + '%091%0D%0A'

            submit_data = f'language=de&bookingtype=Internet&bookingurl=https%3A%2F%2Fwww.qtermin.de%2Fqtermin-stadt-duisburg' \
                          f'-abh-sued&agbaccepted=false&dataprivacyaccepted=true&feedbackpermissionaccepted=false&newsletter' \
                          f'=false&services={sid}&servicestext={servicetext}&servicesinclsgtext={inclsg_text}&FirstName=' \
                          f'{self.user.first_name}&LastName={self.user.last_name}&Email={self.user.email}&Birthday={self.user.birthday}&Street={self.user.street}&ZIP=' \
                          f'{self.user.zipcode}&City={self.user.city}&Phone={self.user.phone}&Salutation={self.user.gender}&Notes=&bookerinfo=Anrede%09' \
                          f'{self.user.gender}%0D%0AVorname%09{self.user.first_name}%0D%0AName%09{self.user.last_name}%0D%0AStrasse%09{self.user.street}%0D%0APLZ%09' \
                          f'{self.user.zipcode}%0D%0AOrt%09{self.user.city}%0D%0ATelefon%09{self.user.phone}%0D%0AE-Mail%09{self.user.email}%0D%0AGeburtsdatum%09' \
                          f'{self.user.birthday}%0D%0A%09%0D%0ATerminerinnerung%0912%20Stunden%20vor%20Termin%0D%0A&calendarname=' \
                          f'{calendarname}&start={start}&end={end}&calendarid={calendarid}&calname={calendarname}&location=' \
                          f'{back_street}&tzaccount=W. Europe Standard Time&checkexist=1&pricegross=0&appgroup=' \
                          f'{self.user.uuid}&capacity=1&servicescapacity={servicescapacity}&servicescapacitydetails=' \
                          f'{servicescapacitydetails}&canceldeadline=0&sync=1&sendemail=1&appointmentreminderhours=-12' \
                          f'&appointmentreminderhours2=-4&confirmappointment=1&confirmtime=120&sendinvoice=1&nrappbooked=1' \
                          f'&capused=false&capmaxused=30&customerconfirm=true&calselid=-1&lnm=1&emailm=1&storeip=false&apw' \
                          f'=false '

            appointment_info, appointment_status = self.post_request(
                "https://www.qtermin.de/api/appointment",
                {
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
                submit_data
            )

            if appointment_status == 200 and appointment_info['StatusMsg'] == 'Appointment created successfully!':
                return True, appointment_info
            else:
                return False, 999
        else:
            return False, 999


class User:
    def __init__(self):
        self.wecom_on, self.wecom_cid, self.wecom_aid, self.wecom_secret, self.wecom_touid, self.item_num, self.close_multi = \
            list(zip(*self.get_config()[0]))[1]
        self.first_name, self.last_name, self.email, self.birthday, self.street, self.zipcode, self.city, self.phone, self.gender, self.expect_date_start, self.expect_date_end = \
            list(zip(*self.get_config()[1]))[1]
        self.uuid = ''.join([self.replacer(c) if c in 'xy' else c for c in 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'])

    @staticmethod
    def get_config():
        pre_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pre_dir, 'config.ini')
        # print(config_path)
        conf = configparser.RawConfigParser()
        conf.read(config_path)
        wecom = conf.items('WecomItem')
        user = conf.items('User')
        return wecom, user

    @staticmethod
    def replacer(n):
        t = int(random.random() * 16)
        i = t if n == 'x' else (t & 3) | 8
        return hex(i)[2:]

    def send_to_wecom(self, text):
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.wecom_cid}&corpsecret={self.wecom_secret}"
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        if access_token and len(access_token) > 0:
            send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
            data = {
                "touser": self.wecom_touid,
                "agentid": self.wecom_aid,
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


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print(str(datetime.now())[0:19] + '>>>📷监控程序启动中...')
    user = User()
    print(str(datetime.now())[0:19] + '>>>📷已读取完成用户信息...')
    position = Position(user)
    print(str(datetime.now())[0:19] + '>>>📷位置获取程序初始化完成...')
    apply = Apply(position, user)
    print(str(datetime.now())[0:19] + '>>>📸启动成功，Ver June.02\n\n')
    user.send_to_wecom('📸启动成功') if user.wecom_on else None
    while position.can_apply is not True and time.strftime('%H:%M', time.localtime()) != '20:26':
        position.if_position()
    if time.strftime('%H:%M', time.localtime()) == '20:26':
        print(str(datetime.now())[0:22] + '>>>💤程序进入重启时间')
        sys.exit()
    print(str(datetime.now())[0:19] + '>>>📖发现位置，正在尝试预约...')
    user.send_to_wecom('✅发现预约位置，正在尝试预约...') if user.wecom_on else None
    position_status, appointment_info = apply.apply()
    outcome = '📤已完成预约\n相关信息如下：\nBuchungsreferenz：' + appointment_info[
        'AdditionalInformation'] if position_status else '❌尝试预约但预约失败，请手动尝试！'
    print(str(datetime.now())[0:19] + '>>>' + outcome)
    user.send_to_wecom(outcome) if user.wecom_on else None


if __name__ == '__main__':
    main()
