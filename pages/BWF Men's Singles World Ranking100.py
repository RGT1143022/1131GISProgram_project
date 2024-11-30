import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")

# 用來儲存日期和ID對應字典
date_id_dict = {}

# 檢查是否已經存儲過第一次爬蟲的資料
if "df_initial" in st.session_state:
    df_initial = st.session_state.df_initial
    date_id_dict = st.session_state.date_id_dict  # 從 session_state 中獲取日期ID對應字典
    st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:")
    st.write(df_initial)

# 第一個按鈕：抓取固定日期11/26/2024資料並取得ID對應字典
if st.button("Get Ranking for 11/26/2024"):
    try:
        # 設定 URL
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"

        # 呼叫第一次爬蟲，獲取排名資料並抓取日期-ID對應字典
        df_initial, date_id_dict = scrape_bwf_ranking(url)

        # 顯示排名資料
        st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:", df_initial)

        # 儲存第一次爬蟲結果到 session_state 中
        st.session_state.df_initial = df_initial
        st.session_state.date_id_dict = date_id_dict  # 儲存日期-ID對應字典

        # 顯示日期選擇表格
        st.write("Available dates for ranking:")
        date_table = pd.DataFrame(list(date_id_dict.items()), columns=["Date", "ID"])
        st.write(date_table)

        # 提示用戶輸入日期
        st.write("Enter a date (e.g., 11/19/2024) to get the ranking:")

        # 用戶輸入日期
        selected_date_input = st.text_input("Enter Date", "")

        # 儲存用戶輸入的日期
        if selected_date_input:
            selected_date_input = selected_date_input.strip()  # 去除多餘的空白
            if selected_date_input in date_id_dict:
                st.session_state.selected_id = date_id_dict[selected_date_input]  # 儲存選擇的 ID
            else:
                st.error("Invalid date entered. Please check the date and try again.")
        
    except Exception as e:
        st.error(f"Error occurred while fetching 11/26/2024 data: {e}")

# 第二個按鈕：根據用戶輸入的日期執行爬蟲
if 'selected_id' in st.session_state and st.button("Get Ranking for Selected Date"):
    try:
        # 取得選擇的日期 ID
        selected_id = st.session_state.selected_id
        
        # 呼叫第二個爬蟲，根據 ID 獲取該日期的資料
        df_selected = scrape_bwf_ranking_by_date(selected_id)

        # 顯示選擇日期的排名資料
        selected_date = list(date_id_dict.keys())[list(date_id_dict.values()).index(selected_id)]  # 取得選擇的日期
        st.write(f"Below is the BWF Men's Singles World Ranking for {selected_date}:", df_selected)

        # 提供下載 CSV 檔案的功能
        st.download_button(
            label="Download CSV for Selected Date",
            data=df_selected.to_csv(index=False),
            file_name=f"bwf_ranking_{selected_date}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error occurred while fetching data for selected date: {e}")
