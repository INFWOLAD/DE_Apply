import time

import requests


def get_request(url, params, headers):
    try:
        response = requests.get(url=url, params=params, headers=headers, verify=False, timeout=4)
        status_code = response.status_code
        return response, status_code
    except:
        print('HTTP Request failed')
        return None, 999


def get_position(first_content, second_content):
    end_content, end_status = get_request(
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


def main(item_num):
    # if __name__ == '__main__':
    #     item_num = 15
    first_status = 0
    second_status = 0
    retry_count = 0
    while first_status + second_status != 400 and retry_count < 2:
        retry_count += 1
        first_response, first_status = get_request(
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

        second_response, second_status = get_request(
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
    try:
        position_data, end_status = get_position(first_response.json()[int(item_num)], second_response.json()[0])
    except:
        end_status = 0
    if end_status == 200:
        # print('正确获取信息')
        return True, position_data.json(), first_response.json()[int(item_num)], second_response.json()[0]
    else:
        # print('获取信息失败')
        return False, 0, 0, 0
