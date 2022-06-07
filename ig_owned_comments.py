"""
Created on 5/21/2022 at 5:36 PM

@author: juanisidro
OneData ©2022
"""
from pandas import concat
from general_utilities import convert_timezone
from ig_tools import get_account_id, get_creds, get_request


fields = (
    "id,comments{"
    "id,timestamp,username,text,like_count}"
    )
account_id = get_account_id('pizzahutrd')
def prep_comments_query(account_id: str, numero_posts: int = 30):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}"
        "/media?"
        f"fields={fields}"
        f"&limit={numero_posts}"
        f"&access_token={token}"
    )
    return url


def get_posts_comments(
        cuenta: str, nposts: int = 30, nperiods: int = 3):
    # cuenta = 'pizzahutrd'
    # nposts = 10
    # nperiods = 3
    results = []
    account_id = get_account_id(cuenta)
    url = prep_comments_query(account_id, nposts)
    while nperiods > -1:
        data, url = get_request(url)
        data = parse_posts_insights(data)
        results.append(data)
        nperiods -= 1
    final_df = concat(results, axis=0, ignore_index=True)
    return final_df
# Gather Post Comments
table = []
url = "https://graph.facebook.com/v13.0/" + account_id + "?fields=media.limit(100){username,timestamp,permalink,id,comments}&access_token=" + token
17841400533223349/media?pretty=0&fields=username%2Ctimestamp%2Cpermalink%2Cid%2Ccomments%7Bid%2Ctimestamp%2Ctext%2Creplies%2Clike_count%2Cusername%7D&limit=1&after=QVFIUkY5RlFVVU5yUmFiaVJpR2FZAVW1hTlBhU2xYTDJ1TFpVOEdVbm8zOF9XN2ItLW42ektlQnExd2ZAKMzBJVmJ1a2lIWWxOSXgyUnllaU41amI4ZAmVXVDdn

17921644535278086/comments?
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
