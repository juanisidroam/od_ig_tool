"""
Created on 5/21/2022 at 5:36 PM

@author: juanisidro
OneData ©2022
"""
from pandas import concat, json_normalize
from general_utilities import convert_timezone
from ig_tools import get_creds, get_comments


fields = (
    "comments.limit(50)"
    "{id,timestamp,username,text,like_count"
    ",replies{id,timestamp,username,text,like_count}"
    "}"
    )


def prep_comments_query(media_id: str):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{media_id}"
        "?"
        f"fields={fields}"
        f"&limit=50"
        f"&access_token={token}"
        )
    return url


def parse_comments(data):
    comments = json_normalize(data)
    try:
        comments.drop('replies.data', inplace=True, axis=1)
    except KeyError:
        pass
    comments.timestamp = comments.timestamp.apply(convert_timezone)
    # for elem in data:
    #     if 'replies' not in elem.keys():
    #         elem.update({"replies": {'data': []}})
    # replies = json_normalize(
    #         data,
    #         record_path=['replies', ['data']],
    #         meta=['id'],
    #         meta_prefix='reply_to_comment_'
    #     )
    # comments = concat([comments, replies], ignore_index=True)
    return comments


def get_posts_comments(media_id: str):
    # media_id = "17926929005103657"
    results = []
    url = prep_comments_query(media_id)
    while url is not None:
        data, url = get_comments(url)
        data = parse_comments(data)
        results.append(data)
    final_df = concat(results, axis=0, ignore_index=True)
    final_df['post_id'] = media_id
    return final_df
