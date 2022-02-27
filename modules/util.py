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
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'] + timedelta(hours = 9) # 日本時間に修正

    df['year'] = df[dt_col].dt.year
    df['month'] = df[dt_col].dt.month
    df['day'] = df[dt_col].dt.day
    # df['dayofweek'] = df[dt_col].dt.dayofweek
    df['dayofweek'] = df[dt_col].dt.day_name()
    df['hour'] = df[dt_col].dt.hour
    df['year_month'] = df['year'].astype(str) + ' ' + df['month'].apply(lambda x: f"{x:02d}")

    return df


# def draw_countplot_year(df, title):
#     order = [i for i in range(df['year'].min(), df['year'].max()+1)]

#     fig = plt.figure()
#     ax = sns.countplot(x=df['year'], order=order)
#     ax.bar_label(ax.containers[0])
#     ax.set_title(title)
#     st.pyplot(fig)

# def draw_countplot_hour(df, title):
#     order = [i for i in range(24)]

#     fig = plt.figure()
#     ax = sns.countplot(x=df['hour'], order=order)
#     # ax.bar_label(ax.containers[0])
#     ax.set_title(title)
#     st.pyplot(fig)


# def draw_countplot_year_month(df, title):
#     year_min = df['year'].min()
#     year_max = df['year'].max()

#     order = []
#     for y in range(year_min, year_max+1):
#         for m in range(1, 13):
#             # don't store less than date of data you have
#             if (y == year_min) and (m < df.sort_index().iloc[0]['month']):
#                 continue
#             # don't store more than current time
#             if (y == year_max) and (m > df.sort_index().iloc[-1]['month']):
#                 continue
#             order.append(f"{y} {m:02d}")

#     fig = plt.figure(figsize=(12, 4))
#     ax = sns.countplot(x=df['year_month'], order=order)
#     ax.set_title(title)
#     plt.xticks(rotation=90)
#     st.pyplot(fig)


# def draw_countplot_dayofweek(df, title):
#     order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#     fig = plt.figure(figsize=(8, 4))
#     ax = sns.countplot(x=df['dayofweek'], order=order)
#     # ax.bar_label(ax.containers[0])
#     ax.set_title(title)
#     st.pyplot(fig)


# def draw_like_browsing_ratio(df, title):
#     fig = plt.figure(figsize=(12, 4))
#     ax = sns.lineplot(data=df.set_index('year_month'))
#     ax.set_title(title)
#     plt.xticks(rotation=90)
#     plt.ylim(ymin=0, ymax=1)
#     plt.grid()
#     ax.get_legend().remove()
#     st.pyplot(fig)
