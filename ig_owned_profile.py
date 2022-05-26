"""
Created on 5/21/2022 at 1:00 AM

@author: juanisidro
OneData ©2022
"""

from ig_owned_daily_insights import get_daily_profile_metrics
from ig_owned_posts_insights import get_posts_metrics
from ig_owned_online_followers import get_online_followers

cuenta = "pizzahutrd"
start_date = "2022-05-5"
end_date = "2022-05-20"

df = get_daily_profile_metrics(cuenta, start_date=start_date, end_date=end_date)
posts = get_posts_metrics(cuenta=cuenta, nposts=30)
#
# writer = pd.ExcelWriter(f'{ig_{cuenta}_page_insights.xlsx', engine='xlsxwriter')
#
# demography.to_excel(writer, sheet_name="IG demography", index=None, header=True)
# geography.to_excel(writer, sheet_name="IG geography", index=None, header=True)
# active.to_excel(writer, sheet_name="IG Online Fans", index=None, header=True)
# pageInsights.to_excel(writer, sheet_name="IG Account Insights", index=None, header=True)
# postInsights.to_excel(writer, sheet_name="IG Media Insights", index=None, header=True)
# postWordList.to_excel(writer, sheet_name="IG Media Word Insights", index=None, header=True)
# postEmojiList.to_excel(writer, sheet_name="IG Media Emoji Insights", index=None, header=True)
# IGcomments.to_excel(writer, sheet_name="IG Comments", index=None, header=True)
# comWordList.to_excel(writer, sheet_name="IG Comment Word List", index=None, header=True)
# comEmojiList.to_excel(writer, sheet_name="IG Comment Emoji List", index=None, header=True)
#
# writer.save()
# writer.close()
#
# if __name__ == "__main__":
#     main()
#
# if __name__ == "__main__":
#     main()
