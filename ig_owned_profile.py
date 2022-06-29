"""
Created on 5/21/2022 at 1:00 AM

@author: juanisidro
OneData ©2022
"""

from pandas import ExcelWriter, concat, DataFrame
from datetime import date, timedelta
from ig_owned_daily_insights import get_daily_profile_metrics
from ig_owned_posts_insights import parse_posts_insights
from ig_owned_online_followers import get_online_followers
from ig_owned_demographics import parse_records, arrange_gender, arrange_provinces
from ig_owned_comments import get_posts_comments
from ig_post_word_extraction import create_emoji_chart, extrae_palabras_claves
from ig_daily_follows import get_followers

from timeit import default_timer as timer
from ig_tools import get_creds, get_account_id
import get_profile_info


def main(cuenta: str = "pizzahutrd", start_date: str = None,
         end_date=None, nposts=100, nperiods=3):
    if not end_date:
        end_date = date.today() - timedelta(1)
        end_date = end_date.strftime('%Y-%m-%d')
    if not start_date:
        start_date = date.fromisoformat(end_date) - timedelta(30)
        start_date = start_date.strftime('%Y-%m-%d')
    token = get_creds()['token']
    cuenta = 'pizzahutrd'
    account_id = get_account_id(cuenta)
    nperiods = 3
    nposts = 100
    print('Process started')
    print(f'Will get {nposts} from {cuenta} and {nperiods} periods')
    result = get_profile_info.main(account_id, token, nposts=nposts)
    print(f'Got profile result')
    profile = result['profile']
    media = result['media']['data']
    demo = result['demo']
    geography = parse_records(demo['data'][0])
    demography = parse_records(demo['data'][2])
    geography = arrange_provinces(geography)
    demography = arrange_gender(demography)
    print(f'Parsed demo/geo')
    post_insights, post_comments = parse_posts_insights(media)
    print(f'Parsed posts')
    mas_50 = post_comments.post_id.value_counts() >= 50
    mas_50 = post_comments.post_id.value_counts()[mas_50].index
    full_comments = [get_posts_comments(c) for c in mas_50]
    print(f'Got all the comments')
    post_comments = concat(full_comments + [post_comments]).drop_duplicates(ignore_index=True)
    post_word_chart = extrae_palabras_claves(post_insights[['post_id', 'caption']])
    print(f'Extracted post words')
    post_emoji_chart = DataFrame(create_emoji_chart(post_insights), columns=['post_id', 'emoji'])
    print(f'Extracted post emoji')
    comment_word_chart = extrae_palabras_claves(post_comments[['post_id', 'text']])
    print(f'Extracted comments words')
    comment_emoji_chart = DataFrame(create_emoji_chart(post_comments, text_col='text'), columns=['post_id', 'emoji'])
    print(f'Extracted comments emoji')
    media_paging = result['media']['paging']['next']


    active = get_online_followers(cuenta)
    print(f'Got online followers')
    daily_follows = get_followers(cuenta)
    print(f'Got daily follows')
    page_insights = get_daily_profile_metrics(cuenta, start_date=start_date, end_date=end_date, nperiods=nperiods)
    print(f'Got daily metrics')


    engine = 'xlsxwriter'
    params = dict(engine=engine, index=None, header=True)
    fecha = date.today().strftime('%Y_%m_%d')
    filename = f'ig_{cuenta}_insights_{fecha}.xlsx'

    with ExcelWriter(filename) as writer:
        profile.to_excel(writer, sheet_name='IG Profile', **params)
        demography.to_excel(writer, sheet_name="IG demography", **params)
        geography.to_excel(writer, sheet_name="IG geography", **params)
        active.to_excel(writer, sheet_name="IG Online Fans", **params)
        daily_follows.to_excel(writer, sheet_name="IG Daily Follows", **params)
        page_insights.to_excel(writer, sheet_name="IG Account Insights", **params)
        post_insights.to_excel(writer, sheet_name="IG Media Insights", **params)
        post_comments.to_excel(writer, sheet_name="IG Media Comments", **params)
        post_word_chart.to_excel(writer, sheet_name="IG Media Word Insights", **params)
        post_emoji_chart.to_excel(writer, sheet_name="IG Media Emoji Insights", **params)
        post_comments.to_excel(writer, sheet_name="IG Comments", **params)
        comment_word_chart.to_excel(writer, sheet_name="IG Comment Word List", **params)
        comment_emoji_chart.to_excel(writer, sheet_name="IG Comment Emoji List", **params)

    writer.save()
    writer.close()


if __name__ == "__main__":
    main()
