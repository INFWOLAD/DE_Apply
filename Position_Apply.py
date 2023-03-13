import requests


def get_request(url, params, headers):
    try:
        response = requests.get(url=url, params=params, headers=headers, verify=False, timeout=4)
        status_code = response.status_code
        return response.json(), status_code
    except:
        print('HTTP Request failed')
        return None, 999


def post_request(url, headers, data):
    try:
        response = requests.post(url=url, headers=headers, data=data, verify=False)
        status_code = response.status_code
        return response.json(), status_code
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return None, 999


def main(position_date, first_content, second_content, first_name, last_name, email, birthday, street, zipcode, city,
         phone, gender, uuid):
    appoint_date, data_status = get_request(
        "https://www.qtermin.de/api/timeslots",
        {
            "date": position_date[0]['start'][0:10],
            "serviceid": first_content['sid'],
            "capacity": "1",
            "caching": "false",
            "duration": first_content['duration'],
            "cluster": "false",
            "slottype": "0",
            "fillcalendarstrategy": "0",
            "showavcap": "false",
            "appfuture": second_content['appfuture'],
            "appdeadline": second_content['appdeadline'],
            "msdcm": second_content['msdcm'],
            "oneoff": "null",
            "appdeadlinewm": second_content['appdeadlinewm'],
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

    location_info, location_status = get_request(
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

    print(appoint_date)
    print(location_info)

    if data_status + location_status == 400:
        sid = first_content['sid']
        servicetext = first_content['s'] + " (1)"
        inclsg_text = first_content['sg'] + '<br>' + first_content['s'] + " (1)"
        calendarname, start, end, calendarid, back_street = appoint_date[0]['calendarname'], appoint_date[0]['start'], \
                                                            appoint_date[0]['end'], appoint_date[0]['calendarid'], \
                                                            location_info[0]['street']
        servicescapacity, servicescapacitydetails = {first_content['sid']: "1"}, first_content['s'] + '%091%0D%0A'

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

        appointment_info, appointment_status = post_request(
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
