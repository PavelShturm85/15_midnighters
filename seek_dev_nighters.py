import pytz
import requests
from datetime import datetime


def load_attempts():
    for page in range(1, 11):
        filter_params = dict(page='{}'.format(page))
        url = 'https://devman.org/api/challenges/solution_attempts'
        solutions_attempts = requests.get(url, params=filter_params).json()
        for attempt in solutions_attempts['records']:
            yield attempt


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
    for name, time in midnighters:
        print('Midnighter name: {}, \t time of sending: {}'.format(name, time))
