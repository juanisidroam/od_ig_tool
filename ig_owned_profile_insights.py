"""
Created on 5/20/2022 at 4:09 AM

@author: juanisidro
OneData ©2022
"""
# needed modules for the whole process
import pandas as pd
from pandas import concat
from ig_tools import get_account_id, prep_query_url, get_request


def deliver_metrics(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    metrics = [
        "reach", 'impressions', 'profile_views', 'follower_count',
        'phone_call_clicks', 'text_message_clicks', 'website_clicks',
        'email_contacts', 'get_directions_clicks']
    if (end_date - start_date).days > 31:
        metrics = [
            "reach", 'impressions', 'profile_views', 'phone_call_clicks',
            'text_message_clicks', 'website_clicks', 'email_contacts',
            'get_directions_clicks']
    return metrics


def process_data(df):
    df.insert(4, "impression_freq", df["impressions"] / df["reach"])
    if "follower_count" in df.columns:
        df.insert(5, "follow_rate", df["follower_count"] / df["reach"])
        df.insert(6, "follow_visit_rate", df["follower_count"] / df["profile_views"])
    return df


def get_daily_profile_metrics(
        cuenta: str, periods: int = 3,
        start_date: str = None, end_date: str = None):
    results = []
    account_id = get_account_id(cuenta)
    metrics = deliver_metrics(start_date, end_date)
    url = prep_query_url(account_id, metrics, start_date, end_date)
    while periods > -1:
        data, url = get_request(url)
        results.append(data)
        periods -= 1
    final_df = concat(results, axis=0, ignore_index=True)
    final_df = process_data(final_df)
    return final_df
