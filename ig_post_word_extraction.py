"""
Created on 5/25/2022 at 11:52 PM

@author: juanisidro
OneData ©2022
"""

import emoji
import spacy
import pandas as pd
nlp = spacy.load("es_dep_news_trf")
# spacy.prefer_gpu()


def extrae_palabras_claves(df):
    lista_palabras = []
    for idx, texto in df.values:
        print(idx, texto)
        doc = nlp(texto.lower())
        pos_list = 'ADV|ADJ|NOUN|VERB|AUX|PRON|PROPN'
        lista = [
            [idx, token.lemma_]
            for token in doc
            if token.pos_ in pos_list
            and token.is_alpha
            and not token.is_stop
            ]
        lista_palabras.extend(lista)
    palabras = pd.DataFrame(lista_palabras, columns=['post_id', 'words'])
    return palabras


def get_emoji(text):
    lista_emoji = emoji.emoji_list(text)
    return [e['emoji'] for e in lista_emoji]


def create_emoji_chart(df):
    df['emoji'] = df['caption'].apply(get_emoji)
    df_list = []
    for idx in df.post_id:
        filtro = df.post_id == idx
        bla = [(idx, a) for a in df.loc[filtro, 'emoji'].values[0]]
        df_list.extend(bla)
    return df_list


def main(df):
    post_word_chart = extrae_palabras_claves(df[['post_id', 'caption']])
    post_emoji_chart = pd.DataFrame(create_emoji_chart(df), columns=['post_id', 'emoji'])
    return post_word_chart, post_emoji_chart
