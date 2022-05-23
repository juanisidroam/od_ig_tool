"""
Created on 5/20/2022 at 4:09 AM

@author: juanisidro
OneData ©2022
"""
# needed modules for the whole process
import pandas as pd
from pandas import concat
from ig_tools import get_account_id, prep_profile_insights_query, get_request, parse_profile_insights


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


def get_daily_profile_metrics(
        cuenta: str, periods: int = 3,
        start_date: str = None, end_date: str = None):
    results = []
    account_id = get_account_id(cuenta)
    metrics = deliver_metrics(start_date, end_date, periods)
    url = prep_profile_insights_query(account_id, metrics, start_date, end_date)
    while periods > -1:
        data, url = get_request(url)
        data = parse_profile_insights(data)
        results.append(data)
        periods -= 1
    final_df = concat(results, axis=0, ignore_index=True)
    return final_df
