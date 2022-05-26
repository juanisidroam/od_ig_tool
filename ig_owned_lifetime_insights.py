"""
Created on 5/21/2022 at 12:59 AM

@author: juanisidro
OneData ©2022
"""

from ig_tools import get_account_id, get_creds, get_request
from pandas import to_datetime, json_normalize
from general_utilities import convert_timezone

# Gather Demography Data



def prep_demographics_query(account_id: str,):
    token = get_creds()['token']
    url = (
        f"https://graph.facebook.com/v13.0/{account_id}"
        "/insights?"
        "metric=audience_city,audience_country,audience_gender_age"
        "&period=lifetime"
        f"&access_token={token}"
    )
    return url


def arrange_provinces(provincias):
    provincias = provincias.join(
        provincias['audience_city']
            .str.split(', ', expand=True)
            .rename({0: 'city', 1:'province'}, axis=1)
    )
    return provincias


def arrange_gender(edad_genero):
    edad_genero = (
        edad_genero['audience_gender_age']
            .str.split('.', expand=True)
            .rename({0: 'gender', 1: 'age'}, axis=1)
            .join(edad_genero)
    ).drop('audience_gender_age', axis=1)
    return edad_genero


def parse_records(data):
    parsed_data = json_normalize(data, record_path=['values']).T
    nombre = data['name']
    request_date = parsed_data.iloc[0][0]
    parsed_data = parsed_data.iloc[1:]
    parsed_data['request_date'] = convert_timezone(request_date)
    parsed_data.index = parsed_data.index.str.replace('value.', '')
    parsed_data.reset_index(inplace=True)
    parsed_data.rename({'index': nombre, 0: 'followers'}, axis=1, inplace=True)
    return parsed_data


def get_demographic_metrics(account):
    token = get_creds()['token']
    account_id = get_account_id(account)
    url = prep_demographics_query(account_id)
    result, paging = get_request(url)
    provincias = parse_records(result[0])
    paises = parse_records(result[1])
    edad_genero = parse_records(result[2])
    provincias = arrange_provinces(provincias)
    edad_genero = arrange_gender(edad_genero)


cuenta = 'pizzahutrd'
get_demographic_metrics(cuenta)



# table = []
# url = "https://graph.facebook.com/v5.0/" + IG_ID + "/insights/audience_gender_age/lifetime?access_token=" + TOKEN
# info = rs.get(url)
# table.append(json.loads(info.text))
#
# demodata = []
# gender = []
# age = []
# followers = []
#
# fields = ["gender", "age", "followers"]
# demodata = list(table[0]["data"][0]["values"][0]["value"])
#
# for a in range(len(demodata)):
#     gender.append(demodata[a].split(".")[0])
#     age.append(demodata[a].split(".")[1])
#
# for b in demodata:
#     followers.append(table[0]["data"][0]["values"][0]["value"][b])
#
# demography = pd.DataFrame([gender, age, followers], fields)
# demography = pd.DataFrame.transpose(demography)
#
# # Gather Geography Data
#
#
# table = []
# url = "https://graph.facebook.com/v5.0/" + IG_ID + "/insights/audience_city/lifetime?access_token=" + TOKEN
# info = rs.get(url)
# table.append(json.loads(info.text))
#
# fields = []
# geodata = []
# cities = []
# provinces = []
# provinces1 = []
# followers = []
#
# fields = ["province", "city", "followers"]
# geodata = list(table[0]["data"][0]["values"][0]["value"])
#
# for a in range(len(geodata)):
#     cities.append(geodata[a].split(",")[0])
#     provinces1.append(geodata[a].split(", ")[1])
#     provinces.append(provinces1[a].split(" Province")[0])
#
# for b in geodata:
#     followers.append(table[0]["data"][0]["values"][0]["value"][b])
#
# geography = pd.DataFrame([provinces, cities, followers], fields)
# geography = pd.DataFrame.transpose(geography)

# Gather Online Activity Data



#
# fields = ["date", "time", "followers"]
# fecha = []
#
# followers = []
# activityData = []
# actData = []

online_followers['weekday'] = online_followers.end_time.dt.day_name()
online_followers['weekday_order'] = online_followers.end_time.dt.weekday
data = online_followers.groupby('weekday').mean().sort_values('weekday_order')

plot(px.density_heatmap(online_followers, y='end_time'))
plot(px.imshow(online_followers.iloc[:,1:]))

plot(px.imshow(data.iloc[:, 1:], y=data.weekday))
plot(px.imshow(data))
# activityData = list(table[0]["data"][0]["values"][0]["value"])

# for a in range(29):
#     for b in table[0]["data"][0]["values"][a]["value"]:
#         activityData.append(table[0]["data"][0]["values"][a]["value"][b])
#
# for c in range(29):
#     fecha.append(table[0]["data"][0]["values"][c]["end_time"].split("T")[0])
#
# actData2 = []
# for i in range(24):
#     for b in range(i, len(activityData), 24):
#         actData2.append(activityData[b])
#
# actData = np.array_split(np.array(actData2), 24)
# actData.insert(0, fecha)
# actData[0] = np.array(actData[0])
# hour.insert(0, "date")
#
# active = pd.DataFrame(actData, hour)
# active = pd.DataFrame.transpose(active)
# active.sort_values

# Set up and export to Excel file
