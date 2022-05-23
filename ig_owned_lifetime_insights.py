"""
Created on 5/21/2022 at 12:59 AM

@author: juanisidro
OneData ©2022
"""



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

if __name__ == "__main__":
    main()
