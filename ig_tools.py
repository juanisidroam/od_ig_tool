"""
Created on 5/20/2022 at 1:22 AM

@author: juanisidro
OneData ©2022
"""

from yaml import safe_load
from requests import get
from datetime import date, timedelta
from pandas import json_normalize, DataFrame, concat

METRICS = ["reach", 'impressions', 'profile_views', 'follower_count',
           'phone_call_clicks', 'text_message_clicks', 'website_clicks',
           'email_contacts', 'get_directions_clicks']
# METRICS = ["reach", 'impressions', 'profile_views',
#            'phone_call_clicks', 'text_message_clicks', 'website_clicks',
#            'email_contacts', 'get_directions_clicks']


def get_creds():
    cred_path = 'creds.yaml'
    with open(cred_path, 'r') as f:
        creds = safe_load(f)
    return creds


TOKEN = get_creds()['facebook_token']['api_key']


def get_account_id(cuenta):
    try:
        ig_id = get(
            "https://graph.facebook.com/v13.0/17841401726234706"
            "?"
            "fields=business_discovery.username(" + cuenta + "){id}&access_token=" + TOKEN
        )
        return ig_id.json()["business_discovery"]["id"]
    except Exception as e:
        print(e)


def prep_query_url(account_id: str, start_date, end_date):
    if not end_date:
        end_date = date.today() - timedelta(1)
        end_date = end_date.strftime('%Y-%m-%d')
    if not start_date:
        start_date = date.fromisoformat(end_date) - timedelta(15)
        start_date = start_date.strftime('%Y-%m-%d')
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}/insights?"
        "metric="
        f"{','.join(METRICS)}"
        "&period=day"
        f"&since={start_date}+&until={end_date}"
        f"&access_token={TOKEN}"
    )
    return url


def get_request(url):
    result = get(url)
    if result.status_code != 200:
        print('Request fallido')
        print(result.text)
    else:
        result = result.json()
        try:
            return parse_ig_data(result['data']), result['paging']['previous']
        except Exception as e:
            print(e)


def parse_ig_data(data):
    insites: DataFrame = (
        json_normalize(data, 'values', ['name'], max_level=10)
        .pivot(index='end_time', columns='name', values='value')
    )
    return insites[METRICS]


def get_daily_profile_metrics(cuenta: str, periods: int = 3,
                              start_date: str = None, end_date: str = None
                              ):
    # cuenta = 'pizzahutrd'
    results = []
    # periods = 5
    account_id = get_account_id(cuenta)
    url = prep_query_url(account_id, start_date, end_date)
    while periods > -1:
        data, url = get_request(url)
        results.append(data)
        periods -= 1
    result = concat(results, axis=0, ignore_index=True)
    return result


if __name__ == "__main__":
    get_creds()
