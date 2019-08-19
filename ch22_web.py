from selenium import webdriver
import time, csv ,os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
def load_web(url):
	# 不打開瀏覽器執行
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	driver = webdriver.Chrome(chrome_options=options)
	driver.maximize_window() #最大化視窗
	driver.set_page_load_timeout(60)  # 等頁面等待載入時間60sec
	driver.get(url) #載入
	# 建立輸入資訊
	start_date = driver.find_element_by_name('fromdate_TextBox')  # 起始日期
	start_date.send_keys('1000101') #輸入日期
	end_date = driver.find_element_by_name('todate_TextBox')  # 結束日期
	end_date.send_keys('1080815')  #輸入日期
	purpose = driver.find_element_by_name('purpose_DDL') # 用途
	purpose.click()
	for option in purpose.find_elements_by_tag_name('option'):  # 記得選elements多項
		if option.text.strip() =='透天住宅':
			option.click()
	submit = driver.find_element_by_name('Submit_Button')  # element不用+s 因為只有一個
	submit.click()
	WebDriverWait(driver, 5).until(
		expected_conditions.presence_of_all_elements_located(
			(By.ID, 'House_GridView')
		)  # 很重要，這個步驟為確認 撈取網站內有你所要爬取的內容 這邊是指表格
	) # 等5秒
	return driver
def data_transfer(web,times,data_df):
	rows = web.find(id='House_GridView').find_all('tr')
	data_key = []  # 裝資料key 要寫在前面會比較清楚
	data_value = []  # 裝資料value
	for row in rows:
		if data_key:
			times+=1
			# 做data_value整理
			values = row.find_all('td')  # 都是數值
			data_value = []  # 清空
			for value in values:
				org_value = value.text.strip().replace(u'\u3000', u'')  # 把空格刪除
				data_value.append(org_value)  # 放入值
			del data_value[0]  # 第一個值是空的清除
			# 將整理完data_value後，將其放入df
			if times == 1: #第一次df
				head = '第' + str(times) + '筆'
				data_df = pd.DataFrame(data_value, columns=[head], index=data_key)
			else: # 第二次以後，直接於df後新增欄
				head = '第' + str(times) + '筆'
				data_df[head] = data_value
		else:  #裡面沒值
			keys = row.find_all('th')  # 都是標題
			for key in keys:
				org_key = key.text.strip().replace(u'\u3000', u'')  # 整理一下key
				data_key.append(org_key)  # 放入key
			del data_key[0]
	return data_df,times
def main():
	url = 'https://www2.bot.com.tw/house/default.aspx'
	try:
		driver = load_web(url)
		# driver.page_source 相當於requests.get後已拿到text再利用 bs4 解析網頁,以html5編碼
		web = BeautifulSoup(driver.page_source, 'html5lib')
		times = 0  # 紀錄次數
		data_df = pd.DataFrame()
		# 第一頁的內容丟進去做整理
		data_df,times = data_transfer(web,times,data_df)
		# 第2頁以後 如要寫多頁 使用while去控制
		driver.find_element_by_xpath('//*[@id="lblNextoneBottom"]').click() #點擊下一頁
		WebDriverWait(driver, 15).until(
			expected_conditions.presence_of_all_elements_located(
				(By.ID, 'House_GridView')
			)  # 撈取爬取內容
		)  # 等5秒
	# 	# driver.page_source 相當於requests.get後已拿到text再利用 bs4 解析網頁,以html5編碼
		web = BeautifulSoup(driver.page_source, 'html5lib')
		data_df,times= data_transfer(web,times,data_df)
		print('總共有 %d 筆'%times)
		print(data_df)
	# 	# 把 dataframe 整理成excel
		os.getcwd() #現在路徑
		data_df.to_csv('法拍屋資訊.csv', encoding = 'utf-8-sig')
		driver.quit()
	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()