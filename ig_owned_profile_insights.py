# needed modules for the whole process
import json
import time

import emoji
import numpy as np
import pandas as pd
import regex
import requests as rs
from ig_tools import get_account_id, get_creds, get_daily_profile_metrics
from datetime import datetime, timedelta

cuenta = "pizzahutrd"
start_date = "2022-05-10"
end_date = "2022-05-19"

pageInsights = get_daily_profile_metrics(cuenta, periods=0)
pageInsights.insert(4, "impression_freq", pageInsights["impressions"] / pageInsights["reach"])
pageInsights.insert(5, "follow_rate", pageInsights["follower_count"] / pageInsights["reach"] * 100)
pageInsights.insert(6, "follow_visit_rate", pageInsights["follower_count"] / pageInsights["profile_views"] * 100)
lel = get_daily_profile_metrics(cuenta, start_date=start_date, end_date=end_date, periods=6)




insites = get_daily_profile_metrics(account_id, start_date=start_date, end_date=end_date)


from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.offline as py
scaler = StandardScaler()



metrics_scaled = pd.DataFrame(
    index=insites.index,
    columns=insites.columns,
    data=scaler.fit_transform(insites)
)


fig = px.line(insites, y=insites.impressions/insites.reach, line_shape='spline')
# fig = px.line(metrics_scaled, line_shape='spline')
# fig = px.line(metrics_scaled)
py.plot(fig)
fig.show()

# fig = px.line(metrics_scaled.rolling(3, min_periods=0).mean())
fig = px.line(metrics_scaled.rolling(3, min_periods=0).mean(), line_shape='spline')
fig = px.line(period_maker(insites.reach), line_shape='spline')
py.plot(fig)


from general_utilities import period_maker

# extracts emoji from text
def split_count(text):
    emoji_list = []
    #     flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text)
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)
    return emoji_list





def get_posts_data():
    ''' Get the specified number of posts from the client's account '''
    url = "https://graph.facebook.com/v5.0/" + IG_ID + "?fields=media.limit(" + str(
        numeroPosts) + "){username,timestamp,permalink,like_count,comments_count,insights.metric(impressions,reach,engagement,saved),media_type,caption,media_url,id}&access_token=" + TOKEN


post_data = rs.get(url).json()
post_insights1 = pd.io.json.json_normalize(post_data["media"]["data"])

# This extracts the insights from the sub lists levels inside the post_data dict
insights = []
for a in range(len(post_data["media"]["data"])):
    temp = {}
    for b in range(4):
        temp[post_data["media"]["data"][a]["insights"]["data"][b]["name"]] = \
        post_data["media"]["data"][a]["insights"]["data"][b]["values"][0]["value"]
    insights.append(temp)

post_insights2 = pd.DataFrame(insights, columns=insights[0].keys())

postInsights = pd.concat([post_insights1.iloc[:, :-1], post_insights2], axis=1)

postInsights["frequency"] = postInsights["impressions"] / postInsights["reach"]
postInsights["impact"] = postInsights["engagement"] / postInsights["reach"].pow(1. / 2)
postInsights["engage %"] = postInsights["engagement"] / postInsights["reach"] * 100
postInsights["saved rate"] = postInsights["saved"] / postInsights["engagement"] * 100

# extract all words from comments
postWords = []
wordLikes = []
wordCom = []
wordSave = []
wordEngage = []
postID = []

for pos, val in enumerate(postInsights['caption']):
    sepaTemp = val.split(" ")
    for b in range(len(sepaTemp)):
        em_split_emoji = emoji.get_emoji_regexp().split(sepaTemp[b])
        for c in em_split_emoji:
            postWords.append(c)
            wordLikes.append(postInsights['like_count'][pos])
            wordCom.append(postInsights['comments_count'][pos])
            wordSave.append(postInsights['saved'][pos])
            wordEngage.append(postInsights['engagement'][pos])
            postID.append(postInsights['id'][pos])

postWordList = pd.DataFrame([postWords, wordLikes, wordCom, wordSave, wordEngage],
                            ["palabras", "likes", "comments", "saves", "engagements"])
postWordList = pd.DataFrame.transpose(postWordList)

# just emoji from comments
postEmoji = []
emojiLikes = []
emojiCom = []
emojiSave = []
emojiEngage = []
postID = []

for pos, val in enumerate(postInsights['caption']):
    try:
        temp = split_count(val)
        for b in temp:
            postEmoji.append(b)
            emojiLikes.append(postInsights['like_count'][pos])
            emojiCom.append(postInsights['comments_count'][pos])
            emojiSave.append(postInsights['saved'][pos])
            emojiEngage.append(postInsights['engagement'][pos])
            postID.append(postInsights['id'][pos])
    except:
        pass

postEmojiList = pd.DataFrame([postEmoji, emojiLikes, emojiCom, emojiSave, emojiEngage],
                             ["emoji", "likes", "comments", "saves", "engagements"])
postEmojiList = pd.DataFrame.transpose(postEmojiList)

# Gather Post Comments
table = []
url = "https://graph.facebook.com/v5.0/" + IG_ID + "?fields=media.limit(100){username,timestamp,permalink,id,comments}&access_token=" + TOKEN
info = rs.get(url)
table.append(json.loads(info.text))

fields = []
valores = []
username = []
fecha = []
permalink = []
comText = []
fechaCom = []
commentID = []
mediaID = []

valores = table[0]["media"]["data"]
# fields = list(valores[0].keys())

for i in range(5):
    fields.append(url[74:114].split(",")[i])

for i in range(10):
    if "comments" in table[0]["media"]["data"][i]:
        tempfield = list(table[0]["media"]["data"][i]["comments"]["data"][0].keys())

fields.append(tempfield)

for c in range(0, len(valores)):
    if "comments" in valores[c]:
        for d in range(len(valores[c]["comments"]["data"])):
            username.append(valores[c]["username"])
            fechaTemp = list(valores[c]["timestamp"])
            fechaTemp[10] = " "
            fecha.append("".join(fechaTemp[0:-5]))
            #             fecha.append(valores[c]["timestamp"].split("T")[0])
            #             hora1 = valores[c]["timestamp"].split("T")[1]
            #             hora1 = hora1.split("+")[0]
            #             hora.append(hora1)
            permalink.append(valores[c]["permalink"])
            mediaID.append(valores[c]["id"])
            fechaTemp1 = list(valores[c]["comments"]["data"][d]["timestamp"])
            fechaTemp1[10] = " "
            fechaCom.append("".join(fechaTemp1[0:-5]))
            comText.append(valores[c]["comments"]["data"][d]["text"])
            commentID.append(valores[c]["comments"]["data"][d]["id"])

fields.remove("timestamp")
fields.insert(1, "post_timestamp")
fields[3] = "media_id"
fields.remove("comments")
fields.insert(4, "comment_text")
fields.insert(5, "comment_timestamp")
fields[6] = "comment_id"

IGcomments = pd.DataFrame([username, fecha, permalink, mediaID, comText, fechaCom, commentID], fields)
IGcomments = pd.DataFrame.transpose(IGcomments)

# extract all words from comments
comWords = []

for a in range(len(comText)):
    sepaTemp = comText[a].split(" ")
    for b in range(len(sepaTemp)):
        em_split_emoji = emoji.get_emoji_regexp().split(sepaTemp[b])
        for b in range(len(em_split_emoji)):
            comWords.append(em_split_emoji[b])

comWordList = pd.DataFrame([comWords], ["palabras comentarios"])
comWordList = pd.DataFrame.transpose(comWordList)

# just emoji from comments
comEmoji = []

for a in range(len(comText)):
    try:
        temp = split_count(comText[a])
        for b in temp:
            comEmoji.append(b)
    except:
        pass

comEmojiList = pd.DataFrame([comEmoji], ["emoji comentarios"])
comEmojiList = pd.DataFrame.transpose(comEmojiList)

# Gather Demography Data

table = []
url = "https://graph.facebook.com/v5.0/" + IG_ID + "/insights/audience_gender_age/lifetime?access_token=" + TOKEN
info = rs.get(url)
table.append(json.loads(info.text))

demodata = []
gender = []
age = []
followers = []

fields = ["gender", "age", "followers"]
demodata = list(table[0]["data"][0]["values"][0]["value"])

for a in range(len(demodata)):
    gender.append(demodata[a].split(".")[0])
    age.append(demodata[a].split(".")[1])

for b in demodata:
    followers.append(table[0]["data"][0]["values"][0]["value"][b])

demography = pd.DataFrame([gender, age, followers], fields)
demography = pd.DataFrame.transpose(demography)

# Gather Geography Data


table = []
url = "https://graph.facebook.com/v5.0/" + IG_ID + "/insights/audience_city/lifetime?access_token=" + TOKEN
info = rs.get(url)
table.append(json.loads(info.text))

fields = []
geodata = []
cities = []
provinces = []
provinces1 = []
followers = []

fields = ["province", "city", "followers"]
geodata = list(table[0]["data"][0]["values"][0]["value"])

for a in range(len(geodata)):
    cities.append(geodata[a].split(",")[0])
    provinces1.append(geodata[a].split(", ")[1])
    provinces.append(provinces1[a].split(" Province")[0])

for b in geodata:
    followers.append(table[0]["data"][0]["values"][0]["value"][b])

geography = pd.DataFrame([provinces, cities, followers], fields)
geography = pd.DataFrame.transpose(geography)

# Gather Online Activity Data


unixdate2 = str(int(time.time()) - 86400)
unixdate1 = str(int(time.time()) - 2678400)

table = []
url = "https://graph.facebook.com/v5.0/" + IG_ID + "/insights?&metric=online_followers&period=lifetime&since=" + unixdate1 + "&until=" + unixdate2 + "&access_token=" + TOKEN
info = rs.get(url)
table.append(json.loads(info.text))

fields = ["date", "time", "followers"]
fecha = []
hour = []
hour1 = []
followers = []
activityData = []
actData = []

hour1 = list(table[0]["data"][0]["values"][4]["value"])
for h in range(24):
    hour1[h] = int(hour1[h])

for i in hour1:
    if i == 9:
        hour.append("12pm")
    if i < 9:
        hour.append(str(i + 3) + "am")
    if 21 > i > 9:
        hour.append(str(i - 9) + "pm")
    if i > 21:
        hour.append(str(i - 21) + "am")
    if i == 21:
        hour.append("12am")

# activityData = list(table[0]["data"][0]["values"][0]["value"])

for a in range(29):
    for b in table[0]["data"][0]["values"][a]["value"]:
        activityData.append(table[0]["data"][0]["values"][a]["value"][b])

for c in range(29):
    fecha.append(table[0]["data"][0]["values"][c]["end_time"].split("T")[0])

actData2 = []
for i in range(24):
    for b in range(i, len(activityData), 24):
        actData2.append(activityData[b])

actData = np.array_split(np.array(actData2), 24)
actData.insert(0, fecha)
actData[0] = np.array(actData[0])
hour.insert(0, "date")

active = pd.DataFrame(actData, hour)
active = pd.DataFrame.transpose(active)
active.sort_values

# Set up and export to Excel file

writer = pd.ExcelWriter("IG " + CUENTA + " page insights.xlsx", engine='xlsxwriter')

demography.to_excel(writer, sheet_name="IG demography", index=None, header=True)
geography.to_excel(writer, sheet_name="IG geography", index=None, header=True)
active.to_excel(writer, sheet_name="IG Online Fans", index=None, header=True)
pageInsights.to_excel(writer, sheet_name="IG Account Insights", index=None, header=True)
postInsights.to_excel(writer, sheet_name="IG Media Insights", index=None, header=True)
postWordList.to_excel(writer, sheet_name="IG Media Word Insights", index=None, header=True)
postEmojiList.to_excel(writer, sheet_name="IG Media Emoji Insights", index=None, header=True)
IGcomments.to_excel(writer, sheet_name="IG Comments", index=None, header=True)
comWordList.to_excel(writer, sheet_name="IG Comment Word List", index=None, header=True)
comEmojiList.to_excel(writer, sheet_name="IG Comment Emoji List", index=None, header=True)

writer.save()
writer.close()