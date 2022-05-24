"""
Created on 5/24/2022 at 5:06 AM

@author: juanisidro
OneData ©2022
"""

from ig_tools import get_account_id, get_creds, get_request
from pandas import json_normalize
from datetime import date, timedelta
from general_utilities import convert_timezone


def create_hour_map():
    hour = {}
    for a in range(24):
        i = str(a)
        if a == 9:
            hour[i] = "12pm"
        if a < 9:
            hour[i] = str(a + 3) + "am"
        if 21 > a > 9:
            hour[i] = str(a - 9) + "pm"
        if a > 21:
            hour[i] = str(a - 21) + "am"
        if a == 21:
            hour[i] = "12am"
    return hour


def prep_online_followers_query(account_id: str):
    token = get_creds()['token']
    # end_date = (date.today()).strftime('%Y-%m-%d')
    end_date = (date.today() - timedelta(3)).strftime('%Y-%m-%d')
    start_date = (date.today() - timedelta(33)).strftime('%Y-%m-%d')
    # start_date = (date.today() - timedelta(31)).strftime('%Y-%m-%d')
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}/insights?"
        "metric=online_followers"
        "&period=lifetime"
        f"&since={start_date}+&until={end_date}"
        f"&access_token={token}"
    )
    return url


def parse_results(online_followers):
    online_followers.columns = online_followers.columns.str.removeprefix('value.')
    online_followers.rename(create_hour_map(), axis=1, inplace=True)
    online_followers.rename({'end_time': 'date'}, axis=1, inplace=True)
    online_followers['date'] = online_followers['date'].apply(convert_timezone).dt.normalize()
    return online_followers


def get_online_followers(cuenta: str):
    account_id = get_account_id(cuenta)
    url = prep_online_followers_query(account_id)
    result = get_request(url)[0]
    online_followers = json_normalize(result, 'values')
    online_followers = parse_results(online_followers)
    return online_followers
