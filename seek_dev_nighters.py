import pytz
import requests
from datetime import datetime


def load_attempts():
    page = 1
    url = 'https://devman.org/api/challenges/solution_attempts'
    while True:
        filter_params = dict(page=page)
        solutions_attempts = requests.get(url, params=filter_params).json()
        page += 1
        yield from solutions_attempts['records']
        if page == solutions_attempts['number_of_pages']:
            break


def get_midnighters_and_time(attempts):
    for attempt in attempts:
        utc_timezone = pytz.timezone('UTC')
        utc_datatime = utc_timezone.localize(
            datetime.utcfromtimestamp(attempt['timestamp']))
        timezone = pytz.timezone(attempt['timezone'])
        data_time = timezone.normalize(utc_datatime.astimezone(timezone))
        hours = datetime.strftime(data_time, "%H")
        if 0 <= int(hours) <= 6:
            yield attempt['username'], datetime.strftime(
                data_time, "%d.%m.%y %H:%M")


if __name__ == '__main__':
    midnighters = get_midnighters_and_time(load_attempts())
    midnighters_list = list(midnighters)
    midnighters_list.sort(key=lambda midnighter: midnighter[0])
    for midnighter in midnighters_list:
        print('Midnighter name: {}, \t time of sending: {}'.format(
            *midnighter))
