import streamlit as st

from zipfile import ZipFile
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

def unzip_and_save_file(filepath, save_dir=None):
    with ZipFile(filepath, 'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        for fileName in listOfFileNames:
            if fileName.endswith('.json'):
                if save_dir is None:
                    zipObject.extract(fileName)
                else:
                    zipObject.extract(fileName, save_dir)


def open_json_file_from_path(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

def open_json_file_from_streamlit_cls(st_cls):
    data = json.load(st_cls)
    return data


def make_date_feature(df, dt_col='Date'):
    df[dt_col] = pd.to_datetime(df[dt_col])
    df[dt_col] = df[dt_col] + timedelta(hours = 9) # 日本時間に修正

    date_attr = ['year', 'month', 'day', 'hour']

    for attr in date_attr:
        df[attr] = getattr(df[dt_col].dt, attr)

    # df['dayofweek'] = df[dt_col].dt.dayofweek
    df['dayofweek'] = df[dt_col].dt.day_name()
    df['year_month'] = df['year'].astype(str) + ' ' + df['month'].apply(lambda x: f"{x:02d}")

    return df
