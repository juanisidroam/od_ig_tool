"""
Created on 5/20/2022 at 1:22 AM

@author: juanisidro
OneData ©2022
"""

from yaml import safe_load
from requests import get
from datetime import date, timedelta
from pandas import json_normalize, DataFrame, merge

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


def prep_profile_insights_query(account_id: str, metrics, start_date, end_date):
    token = get_creds()['token']
    if not end_date:
        end_date = date.today() - timedelta(1)
        end_date = end_date.strftime('%Y-%m-%d')
    if not start_date:
        start_date = date.fromisoformat(end_date) - timedelta(15)
        start_date = start_date.strftime('%Y-%m-%d')
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}/insights?"
        "metric="
        f"{','.join(metrics)}"
        "&period=day"
        f"&since={start_date}+&until={end_date}"
        f"&access_token={token}"
    )
    return url


def prep_profile_posts_query(account_id: str, fields, numero_posts: int = 30):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}"
        "?fields=media.limit"
        f"({numero_posts})"
        f"{fields}"
        f"&access_token={token}"
    )
    return url


def get_request(url):
    result = get(url)
    if result.status_code != 200:
        print('Request fallido')
        print(result.text)
    else:
        result = result.json()
        if 'media' in result.keys():
            data = result['media']['data']
            paging_next = result['media']['paging']['next']
        else:
            data = result['data']
            paging_next = result['paging']['next']
        return data, paging_next


def parse_profile_insights(data):
    df: DataFrame = (
        json_normalize(
            data,
            record_path='values',
            meta=['name'],
            errors='ignore'
            )
        .pivot(index='end_time', columns='name', values='value')
    )
    return df


def parse_posts_insights(data):
    posts = json_normalize(
            data,
            max_level=0
            )
    posts.drop('insights', inplace=True, axis=1)
    posts.rename(columns = {'id':'post_id'}, inplace=True)
    metrics = json_normalize(
            data=data,
            record_path=['insights', ['data']],
            meta=['id'],
            meta_prefix='post_'
    )
    metrics['values'] = metrics['values'].apply(lambda x: x[0]['value'])
    metrics = metrics.pivot(columns='name', values='values', index='post_id')
    metrics.reset_index(inplace=True)
    df = merge(posts, metrics, on='post_id')
    return df
