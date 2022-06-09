"""
Created on 6/7/2022 at 11:06 PM

@author: juanisidro
OneData ©2022
"""
from requests import get
from pandas import Series

profile_fields = (
    "username,name,id,ig_id,website,followers_count"
    ",follows_count,media_count,profile_picture_url,biography"
    )

insight_fields = (
    '(reach,impressions,profile_views,follower_count'
    ',phone_call_clicks,text_message_clicks,'
    'website_clicks,email_contacts,get_directions_clicks)'
    )

media_fields = (
    "{username,timestamp,permalink"
    ",media_type,caption,media_url,id"
    ",like_count,comments_count"
    ",insights.metric(impressions,reach,engagement,saved)"
    ",comments.limit(50){id,timestamp,username,text,like_count}}"
    )


def prep_profile_info_query(account_id, token, nposts):
    if not token:
        print('This module needs a token')
    else:
        url = (
            f"https://graph.facebook.com/v13.0/{account_id}?"
            f"fields={profile_fields}"
            f",insights.metric(audience_city,audience_country,audience_gender_age).period(lifetime)"
            f",media.limit({nposts}){media_fields}"
            f"&access_token={token}"
            )
        return url


def get_main_request(url):
    result = get(url)
    if result.status_code != 200:
        print('Request fallido')
        print(result.text)
    else:
        result = result.json()
        return result


def main(account_id, token, nposts=100):
    # cuenta = 'pizzahutrd'
    # token = get_creds()['token']
    # account_id = get_account_id(cuenta)
    url = prep_profile_info_query(account_id, token, nposts)
    result = get_main_request(url)
    profile = Series({k: result[k] for k in result.keys() if k in profile_fields.split(',')})
    data = {
        'profile': profile,
        'demo': result['insights'],
        'media': result['media']
        }
    return data
