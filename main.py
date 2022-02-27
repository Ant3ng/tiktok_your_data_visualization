import streamlit as st
import os
from PIL import Image

from modules.util import *
from modules.plot_func import *


new_line = '  \n  '

################################################################################################
###### Sidebar notes
################################################################################################

image = Image.open('image/mans_search_for_movie.jpg')
st.sidebar.image(image)

st.sidebar.title("")
st.sidebar.markdown("TikTokの自分のアカウントデータを可視化するページ")
st.sidebar.markdown("You'll see some graphs of your TikTok account data")

st.sidebar.markdown("## Link")
st.sidebar.markdown("[note](https://note.com/t_and/n/n18d335dd068e)")
st.sidebar.markdown("[github](xxxxx)")



################################################################################################
###### Intro
################################################################################################

st.markdown("### TikTokの自分のアカウントデータを可視化するページ")
st.markdown("### You'll see some graphs of your TikTok account data")

st.write('-'*50)

st.markdown("#### 可視化される内容 / Graphs you can see")
st.write('以下のページにあるようなグラフを見ることができます。')
st.write('You upload your data and get to see graphs like page below')

st.write("[noteのページ](https://note.com/t_and/n/n18d335dd068e#4VNxw)")


st.write('-'*50)


################################################################################################
###### How to get data
################################################################################################

st.markdown("#### データの取得方法 / How to download your data")
st.write('以下のステップを踏むことでデータを取得できます。注意点としてTXTとJSONのうちJSONデータを選択してください。申請から2, 3日でデータのダウンロードが可能になります。')
st.write('You can download by taking following step. Note you should select JSON format. TXT format is not allowed to make graphs. After request, it will be available to download in the next few days')

st.image(Image.open('image/how_to_get_data_01.png'))
st.image(Image.open('image/how_to_get_data_02.png'))

st.write('ダウンロードするとZipファイルが保存され、それを開くとJSONファイルを得ることができます。なお、次のステップではファイルをアップロードしますが、ZipとJSONのどちらでも構いません。')
st.write('After download, you get a JSON file compressed into Zip format. In next upload step, both of formats are fine')

st.write('-'*50)


################################################################################################
###### Upload files
################################################################################################

st.markdown("#### データのアップロード＆可視化 / Upload and Graphs")
st.write('↓ ZipもしくはJsonのファイルをアップロードする ↓')

uploaded_file = st.file_uploader('Upload Zip or Json file downloaded via TikTok', type=['zip', 'json'])

st.write('アップロードしたデータは可視化後に消去されます')
st.write('Data you upload will be deleted after graphs plotted. No worry')

if uploaded_file is not None:

    if uploaded_file.type == 'application/zip':
        unzip_and_save_file(uploaded_file)
        json_data = open_json_file_from_path('user_data.json')
    elif uploaded_file.type == 'application/json':
        json_data = open_json_file_from_streamlit_cls(uploaded_file)
    else:
        # Zip/Json以外選択できないようになるっぽいので、不要かも
        st.write(f"アップロードしたファイルはZip, Jsonの形式ではないようです。{new_line}Uploaded data format doesn't meet requirement to visualize. Only Zip/Json format is allowed")


    ################################################################################################
    ###### Following list
    ################################################################################################

    mod_data = pd.DataFrame(json_data['Activity']['Following List']['Following']).sort_values('Date').reset_index(drop=True)
    mod_data = make_date_feature(mod_data)

    st.write('-'*50)
    st.markdown(f"#### フォロー履歴 / Following List")
    st.write(f"UserNameが空欄のものは、UserNameが初期値/未設定のものだと考えられる{new_line}Maybe blank name is not named yet")
    st.dataframe(mod_data[['Date', 'UserName']])

    draw_countplot_year(mod_data, title=f"Number of followings every year (Total = {len(mod_data)})")
    draw_countplot_hour(mod_data, title="Number of total followings every hour")
    draw_countplot_year_month(mod_data, title="Number of followings every year-month")
    draw_countplot_dayofweek(mod_data, title="Number of total followings every dayofweek")


    ################################################################################################
    ###### Like list
    ################################################################################################

    mod_data = pd.DataFrame(json_data['Activity']['Like List']['ItemFavoriteList']).sort_values('Date').reset_index(drop=True)
    mod_data = make_date_feature(mod_data)

    st.write('-'*50)
    st.markdown(f"#### いいね履歴 / Like List")
    st.write(f"初期のデータが入っていないことがあるが、仕様と思われる。URLが途中で切れている場合、右側に表示されている矢印をクリックすると全て表示される")
    st.write(f"Early data might be missing and It's not clear why. In order to see full VideoLink, click 'View fullscreen'")
    st.dataframe(mod_data[['Date', 'VideoLink']].sort_index())

    draw_countplot_year(mod_data, title=f"Number of likes every year (Total = {len(mod_data)})")
    draw_countplot_hour(mod_data, title="Number of total likes every hour")
    draw_countplot_year_month(mod_data, title="Number of likes every year-month")
    draw_countplot_dayofweek(mod_data, title="Number of total likes every dayofweek")


    ################################################################################################
    ###### Video Browsing History
    ################################################################################################
    mod_data = pd.DataFrame(json_data['Activity']['Video Browsing History']['VideoList']).sort_values('Date').reset_index(drop=True)
    mod_data = make_date_feature(mod_data)

    st.write('-'*50)
    st.markdown(f"#### 視聴履歴 / Video Browsing History")
    st.write(f"初期のデータが入っていないことがあるが、仕様と思われる。URLが途中で切れている場合、右側に表示されている矢印をクリックすると全て表示される。同時刻に複数データが入っていることがある。つまり、0秒でスワイプした動画も含まれている。")
    st.write(f"Early data might be missing and It's not clear why. In order to see full VideoLink, click 'View fullscreen'. You might find multiple data at the same time. It means even if you just swipe video, it is counted as 'watched'")
    st.dataframe(mod_data[['Date', 'VideoLink']].sort_index())

    draw_countplot_year(mod_data, title=f"Number of browsing every year (Total = {len(mod_data)})")
    draw_countplot_hour(mod_data, title="Number of total browsing every hour")
    draw_countplot_year_month(mod_data, title="Number of browsing every year-month")
    draw_countplot_dayofweek(mod_data, title="Number of total browsing every dayofweek")


    ################################################################################################
    ###### Like / Browsing Ratio
    ################################################################################################
    like_data = pd.DataFrame(json_data['Activity']['Like List']['ItemFavoriteList']).sort_values('Date').reset_index(drop=True)
    like_data = make_date_feature(like_data).sort_index()

    browsing_data = pd.DataFrame(json_data['Activity']['Video Browsing History']['VideoList']).sort_values('Date').reset_index(drop=True)
    browsing_data = make_date_feature(browsing_data).sort_index()

    # Early data might be missing, so adjust date to give accurate ratio
    min_max_date = max(like_data['Date'].min(), browsing_data['Date'].min())
    like_data = like_data.query("Date >= @min_max_date")
    browsing_data = browsing_data.query("Date >= @min_max_date")

    like_browsing_ratio = like_data.groupby('year_month').size() / browsing_data.groupby('year_month').size()
    like_browsing_ratio.fillna(0, inplace=True)

    # You might not use TikTok some year-month. That leads to missing year-month
    # Process below is about imputation of these missing.
    max_date = max(like_data['Date'].max(), browsing_data['Date'].max())
    date_list = []
    for y in range(min_max_date.year, max_date.year+1):
        for m in range(1, 13):
            if (y == min_max_date.year) and (m < min_max_date.month):
                continue
            if (y == max_date.year) and (m > max_date.month):
                continue
            date_list.append(f"{y} {m:02d}")

    date_df = pd.DataFrame(date_list, columns=['year_month'])
    like_browsing_ratio = date_df.merge(like_browsing_ratio.reset_index(), 'left', 'year_month')

    st.write('-'*50)
    st.markdown(f"#### 視聴数に対するいいねの割合 / Ratio of likes to views")
    draw_like_browsing_ratio(like_browsing_ratio, title='Ratio of likes to views')

    ################################################################################################
    ###### Delete Uploaded Data
    ################################################################################################
    # ZipファイルをUploadした時のみ、JsonファイルがSaveされる
    # そのため、消去するのはZipファイルを選択した時のみで良い

    if uploaded_file.type == 'application/zip':
        os.remove('user_data.json')

    st.write('-'*50)
    st.markdown(f"#### おしまい / Done")



