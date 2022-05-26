"""
Created on 5/21/2022 at 12:58 AM

@author: juanisidro
OneData ©2022
"""
from pandas import concat, json_normalize, merge
from ig_tools import get_account_id, get_creds, get_request
from general_utilities import convert_timezone

fields = (
    "username,timestamp,permalink"
    ",media_type,caption,media_url,id"
    ",like_count,comments_count"
    ",insights.metric(impressions,reach,engagement,saved)"
    )


def prep_profile_posts_query(account_id: str, numero_posts: int = 30):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}"
        "/media?"
        f"fields={fields}"
        f"&limit={numero_posts}"
        f"&access_token={token}"
    )
    return url


def parse_posts_insights(data):
    posts = json_normalize(
            data,
            max_level=0
            )
    posts.drop('insights', inplace=True, axis=1)
    posts.rename(columns={'id': 'post_id'}, inplace=True)
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
    df.timestamp = df.timestamp.apply(convert_timezone)
    return df


def get_posts_metrics(
        cuenta: str, nposts: int = 30, nperiods: int = 3):
    cuenta = 'pizzahutrd'
    nposts = 10
    nperiods = 3
    results = []
    account_id = get_account_id(cuenta)
    url = prep_profile_posts_query(account_id, nposts)
    while nperiods > -1:
        data, url = get_request(url)
        data = parse_posts_insights(data)
        results.append(data)
        nperiods -= 1
    final_df = concat(results, axis=0, ignore_index=True)
    return final_df
