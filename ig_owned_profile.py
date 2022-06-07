"""
Created on 5/21/2022 at 1:00 AM

@author: juanisidro
OneData ©2022
"""

from pandas import ExcelWriter
from datetime import date
from ig_owned_daily_insights import get_daily_profile_metrics
from ig_owned_posts_insights import get_posts_metrics
from ig_owned_online_followers import get_online_followers
from ig_owned_demographics import get_demographic_metrics
import ig_post_word_extraction

cuenta = "pizzahutrd"
start_date = "2022-03-20"
end_date = "2022-05-20"

# df = get_daily_profile_metrics(cuenta, start_date=start_date, end_date=end_date)
# posts = get_posts_metrics(cuenta=cuenta, nposts=30)

geography, demography = get_demographic_metrics(cuenta)
active = get_online_followers(cuenta)
page_insights = get_daily_profile_metrics(cuenta)
post_insights = get_posts_metrics(cuenta)
# online_followers['weekday'] = online_followers.end_time.dt.day_name()
# online_followers['weekday_order'] = online_followers.end_time.dt.weekday
# data = online_followers.groupby('weekday').mean().sort_values('weekday_order')
#
# plot(px.density_heatmap(online_followers, y='end_time'))
# plot(px.imshow(online_followers.iloc[:,1:]))
#
# plot(px.imshow(data.iloc[:, 1:], y=data.weekday))
# plot(px.imshow(data))
#

engine = 'xlsxwriter'
params = dict(engine=engine, index=None, header=True)


fecha = date.today().strftime('%Y_%m_%d')
filename = f'ig_{cuenta}_insights_{fecha}.xlsx'

with ExcelWriter(filename) as writer:
    demography.to_excel(writer, sheet_name="IG demography", engine=engine, index=None, header=True)
    geography.to_excel(writer, sheet_name="IG geography", engine=engine, index=None, header=True)
    active.to_excel(writer, sheet_name="IG Online Fans", engine=engine, index=None, header=True)
    page_insights.to_excel(writer, sheet_name="IG Account Insights", engine=engine, index=None, header=True)
    post_insights.to_excel(writer, sheet_name="IG Media Insights", engine=engine, index=None, header=True)
    # postWordList.to_excel(writer, sheet_name="IG Media Word Insights", engine=engine, index=None, header=True)
    # postEmojiList.to_excel(writer, sheet_name="IG Media Emoji Insights", engine=engine, index=None, header=True)
    # IGcomments.to_excel(writer, sheet_name="IG Comments", engine=engine, index=None, header=True)
    # comWordList.to_excel(writer, sheet_name="IG Comment Word List", engine=engine, index=None, header=True)
    # comEmojiList.to_excel(writer, sheet_name="IG Comment Emoji List", engine=engine, index=None, header=True)
#
# writer.save()
# writer.close()
#
# if __name__ == "__main__":
#     main()
#
# if __name__ == "__main__":
#     main()
