"""
Created on 5/21/2022 at 5:36 PM

@author: juanisidro
OneData ©2022
"""



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


# extracts emoji from text
def split_count(text):
    emoji_list = []
    #     flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text)
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)
    return emoji_list



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



if __name__ == "__main__":
    main()
