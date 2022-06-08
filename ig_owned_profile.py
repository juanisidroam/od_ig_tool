"""
Created on 5/21/2022 at 1:00 AM

@author: juanisidro
OneData ©2022
"""

from pandas import ExcelWriter, concat, DataFrame
from datetime import date, timedelta
from ig_owned_daily_insights import get_daily_profile_metrics
from ig_owned_posts_insights import get_posts_metrics
from ig_owned_online_followers import get_online_followers
from ig_owned_demographics import get_demographic_metrics
from ig_owned_comments import get_posts_comments
from ig_post_word_extraction import create_emoji_chart, extrae_palabras_claves


def main(cuenta: str = "pizzahutrd", start_date: str = None,
         end_date=None, nposts=30, nperiods=0):
    if not end_date:
        end_date = date.today() - timedelta(1)
        end_date = end_date.strftime('%Y-%m-%d')
    if not start_date:
        start_date = date.fromisoformat(end_date) - timedelta(30)
        start_date = start_date.strftime('%Y-%m-%d')
    geography, demography = get_demographic_metrics(cuenta)
    active = get_online_followers(cuenta)
    page_insights = get_daily_profile_metrics(cuenta, start_date=start_date, end_date=end_date, nperiods=nperiods)
    post_insights, post_comments = get_posts_metrics(cuenta, nposts=nposts, nperiods=nperiods)
    mas_50 = post_comments.post_id.value_counts() >= 50
    mas_50 = post_comments.post_id.value_counts()[mas_50].index
    full_comments = [get_posts_comments(c) for c in mas_50]
    post_comments = concat(full_comments + [post_comments]).drop_duplicates(ignore_index=True)
    post_word_chart = extrae_palabras_claves(post_insights[['post_id', 'caption']])
    post_emoji_chart = DataFrame(create_emoji_chart(post_insights), columns=['post_id', 'emoji'])
    comment_word_chart = extrae_palabras_claves(post_comments[['post_id', 'text']])
    comment_emoji_chart = DataFrame(create_emoji_chart(post_comments, text_col='text'), columns=['post_id', 'emoji'])

    engine = 'xlsxwriter'
    params = dict(engine=engine, index=None, header=True)
    fecha = date.today().strftime('%Y_%m_%d')
    filename = f'ig_{cuenta}_insights_{fecha}.xlsx'

    with ExcelWriter(filename) as writer:
        demography.to_excel(writer, sheet_name="IG demography", **params)
        geography.to_excel(writer, sheet_name="IG geography", **params)
        active.to_excel(writer, sheet_name="IG Online Fans", **params)
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
