"""
Created on 6/28/2022 at 9:07 PM

@author: juanisidro
OneData ©2022
"""

from ig_tools import get_account_id, get_request, get_creds
from datetime import date, timedelta
from pandas import json_normalize, concat, DataFrame
from general_utilities import convert_timezone


start_date = date.today() - timedelta(29)
end_date = date.today() + timedelta(1)

def prep_profile_insights_query(account_id: str):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}/insights?"
        "metric="
        f"follower_count"
        "&period=day"
        f"&since={start_date}&until={end_date}"
        f"&access_token={token}"
        )
    return url

def parse_profile_insights(data):
    df: DataFrame = (
        json_normalize(
            data,
            record_path='values',
            meta=['name'],
            errors='ignore'
            )
        .pivot(index='end_time', columns='name', values='value')
        ).reset_index()
    df.end_time = df.end_time.apply(convert_timezone).dt.normalize()
    return df

def get_followers(cuenta: str):
    cuenta = 'pizzahutrd'
    results = []
    account_id = get_account_id(cuenta)
    url = prep_profile_insights_query(account_id)
    try:
        data, url = get_request(url)
    except TypeError as e:
        print(e)
    data = parse_profile_insights(data)
    return data



