"""
Created on 5/20/2022 at 1:22 AM

@author: juanisidro
OneData ©2022
"""

from yaml import safe_load
from requests import get
# from datetime import date, timedelta
# from pandas import json_normalize, DataFrame, merge

# METRICS = ["reach", 'impressions', 'profile_views', 'follower_count',
#            'phone_call_clicks', 'text_message_clicks', 'website_clicks',
#            'email_contacts', 'get_directions_clicks']
# METRICS = ["reach", 'impressions', 'profile_views',
#            'phone_call_clicks', 'text_message_clicks', 'website_clicks',
#            'email_contacts', 'get_directions_clicks']


def extract_new_profile_metrics(df):
    df.insert(4, "impression_freq", df["impressions"] / df["reach"])
    if "follower_count" in df.columns:
        df.insert(5, "follow_rate", df["follower_count"] / df["reach"])
        df.insert(6, "follow_visit_rate", df["follower_count"] / df["profile_views"])
    return df


def extract_new_posts_metrics(df):
    df["post_frequency"] = df["impressions"] / df["reach"]
    df["post_impact"] = df["engagement"] / df["reach"].pow(1. / 2)
    df["engage_percent"] = df["engagement"] / df["reach"]
    df["saved_rate"] = df["saved"] / df["reach"]
    return df


def get_creds():
    cred_path = 'creds.yaml'
    with open(cred_path, 'r') as f:
        creds = safe_load(f)
    return creds


def get_account_id(cuenta):
    token = get_creds()['token']
    try:
        ig_id = get(
            "https://graph.facebook.com/v13.0/17841401726234706"
            "?"
            "fields=business_discovery.username(" + cuenta + "){id}&access_token=" + token
        )
        return ig_id.json()["business_discovery"]["id"]
    except Exception as e:
        print(e)


def get_request(url):
    result = get(url)
    if result.status_code != 200:
        print('Request fallido')
        print(result.text)
    else:
        result = result.json()
        # if 'media' in result.keys():
        #     data = result['media']['data']
        #     paging_next = result['media']['paging']['next']
        # else:
        #     data = result['data']
        #     paging_next = result['paging']['next']
        # return data, paging_next
        data = result['data']
        paging_next = result['paging']['next']
        return data, paging_next
