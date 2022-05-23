"""
Created on 5/21/2022 at 12:58 AM

@author: juanisidro
OneData ©2022
"""
from pandas import concat
from ig_tools import get_account_id, prep_profile_posts_query, get_request, parse_posts_insights

fields = (
    "{username,timestamp,permalink"
    ",insights.metric(impressions,reach,engagement,saved)"
    ",media_type,caption,media_url,id"
    ",like_count,comments_count}"
    )


def get_posts_metrics(
        cuenta: str, nposts: int = 30, nperiods: int = 3):
    # cuenta = 'pizzahutrd'
    # nposts = 10
    # nperiods = 3
    results = []
    account_id = get_account_id(cuenta)
    url = prep_profile_posts_query(account_id, fields, nposts)
    while nperiods > -1:
        data, url = get_request(url)
        data = parse_posts_insights(data)
        results.append(data)
        nperiods -= 1
    final_df = concat(results, axis=0, ignore_index=True)
    return final_df
