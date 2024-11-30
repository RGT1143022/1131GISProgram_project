from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_bwf_ranking():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 打開目標網站
        url = "https://bwf.tournamentsoftware.com/ranking/ranking.aspx?rid=70"
        page.goto(url)

        # 點擊 "Men's Singles" 分頁
        page.click("text=Men's Singles")

        # 點擊多次 "More" 按鈕以加載更多數據
        while True:
            try:
                page.click("text=More", timeout=3000)
            except:
                break

        # 提取表格數據
        rows = page.query_selector_all("table.ruler tbody tr")
        data = []
        for row in rows:
            cols = row.query_selector_all("td")
            data.append([col.inner_text().strip() for col in cols])

        browser.close()

    # 保存結果到 CSV
    columns = ["Rank", "Player", "Country", "Points", "Tournaments"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("bwf_ranking.csv", index=False)

if __name__ == "__main__":
    scrape_bwf_ranking()
