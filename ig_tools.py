"""
Created on 5/20/2022 at 1:22 AM

@author: juanisidro
OneData ©2022
"""

from yaml import safe_load
from requests import get


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
            "fields=business_discovery"
            f".username({cuenta})"
            "{id}"
            f"&access_token={token}"
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
        data = result['data']
        try:
            if 'since' in url:
                paging_next = result['paging']['previous']
            else:
                paging_next = result['paging']['next']
        except KeyError:
            paging_next = None
        return data, paging_next


def get_comments(url):
    result = get(url)
    if result.status_code != 200:
        print('Request fallido')
        print(result.text)
    else:
        result = result.json()
        try:
            data = result['comments']['data']
        except KeyError:
            data = result['data']
        try:
            paging_next = result['comments']['paging']
            try:
                paging_next = paging_next['next']
            except KeyError:
                paging_next = None
        except KeyError:
            try:
                paging_next = result['paging']['next']
            except KeyError:
                paging_next = None
        return data, paging_next
