"""
Created on 5/20/2022 at 4:09 AM

@author: juanisidro
OneData ©2022
"""
# needed modules for the whole process
import pandas as pd
from pandas import json_normalize, concat, DataFrame
from datetime import date, timedelta
from ig_tools import get_account_id, get_creds, get_request


def deliver_metrics(start_date, end_date, periods):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    amount_of_days = (end_date - start_date).days * periods
    metrics = [
        "reach", 'impressions', 'profile_views', 'follower_count',
        'phone_call_clicks', 'text_message_clicks', 'website_clicks',
        'email_contacts', 'get_directions_clicks']
    if amount_of_days > 31:
        metrics = [
            "reach", 'impressions', 'profile_views', 'phone_call_clicks',
            'text_message_clicks', 'website_clicks', 'email_contacts',
            'get_directions_clicks']
    return metrics


def prep_profile_insights_query(account_id: str, metrics, start_date, end_date):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}/insights?"
        "metric="
        f"{','.join(metrics)}"
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
    )
    return df


def get_daily_profile_metrics(
        cuenta: str, periods: int = 3,
        start_date: str = None, end_date: str = None):
    cuenta = 'pizzahutrd'
    periods = 3
    if not end_date:
        end_date = date.today() - timedelta(1)
        end_date = end_date.strftime('%Y-%m-%d')
    if not start_date:
        start_date = date.fromisoformat(end_date) - timedelta(15)
        start_date = start_date.strftime('%Y-%m-%d')
    results = []
    account_id = get_account_id(cuenta)
    metrics = deliver_metrics(start_date, end_date, periods)
    url = prep_profile_insights_query(account_id, metrics, start_date, end_date)
    while periods > -1:
        data, url = get_request(url)
        data = parse_profile_insights(data)
        results.append(data)
        periods -= 1
        if not url:
            break
    final_df = concat(results, axis=0, ignore_index=True)
    return final_df
