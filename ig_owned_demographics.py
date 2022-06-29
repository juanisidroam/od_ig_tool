"""
Created on 5/21/2022 at 12:59 AM

@author: juanisidro
OneData ©2022
"""

from ig_tools import get_account_id, get_creds, get_request
from pandas import json_normalize
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
        .rename({0: 'city', 1: 'province'}, axis=1)
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
    parsed_data['request_date'] = convert_timezone(request_date).date()
    parsed_data.index = parsed_data.index.str.replace('value.', '')
    parsed_data.reset_index(inplace=True)
    parsed_data.rename({'index': nombre, 0: 'followers'}, axis=1, inplace=True)
    return parsed_data


def get_demographic_metrics(account) -> tuple:
    account_id = get_account_id(account)
    url = prep_demographics_query(account_id)
    result, paging = get_request(url)
    provincias = parse_records(result[0])
    # paises = parse_records(result[1])
    edad_genero = parse_records(result[2])
    provincias = arrange_provinces(provincias)
    edad_genero = arrange_gender(edad_genero)
    return provincias, edad_genero
