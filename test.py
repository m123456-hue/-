from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver-win64', 'chromedriver.exe')
chrome_options = Options()
# 不加无头模式，弹窗可视化浏览器
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 40)

driver.get("https://www.chinamoney.com.cn/english/bdInfo/")

print("请在弹出的浏览器窗口中手动选择筛选条件（Bond Type= Treasury Bond, Issue Year=2023），点击Search，等待表格加载出来后，回到此窗口按回车继续...")
input("表格加载完成后请按回车：")

all_data = []
headers = []
page = 1
while True:
    try:
        # 定位表格
        sheet = driver.find_element(By.CSS_SELECTOR, 'div.san-datasheet table.san-sheet-alternating')
        # 表头
        thead = sheet.find_element(By.TAG_NAME, 'thead')
        header_cells = thead.find_elements(By.TAG_NAME, 'td')
        headers = [cell.text.strip() for cell in header_cells]
        # 数据行
        tbody = sheet.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            data.append([cell.text.strip() for cell in cells])
        # 只保留指定列
        wanted_cols = ["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"]
        col_idx = [headers.index(col) for col in wanted_cols if col in headers]
        filtered_headers = [headers[i] for i in col_idx]
        filtered_data = [[row[i] for i in col_idx] for row in data]
        all_data.extend(filtered_data)
        print(f"已抓取第{page}页, 当前累计{len(all_data)}条数据")
        # 判断是否有“Next”按钮可点击
        next_btn = driver.find_element(By.CSS_SELECTOR, 'li.page-btn.page-next:not(.disabled)')
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        next_btn.click()
        time.sleep(2)  # 等待新页面加载
        page += 1
    except Exception as e:
        print("已到最后一页或翻页出错：", e)
        break

if all_data:
    df = pd.DataFrame(all_data, columns=filtered_headers)
    df.to_csv("china_treasury_bonds_2023_all.csv", index=False, encoding="utf-8-sig")
    print("已保存所有页数据为 china_treasury_bonds_2023_all.csv")
    print("总数据条数：", len(all_data))
else:
    print("未抓取到任何数据！")
driver.quit()

















