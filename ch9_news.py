import re,json
import requests
from bs4 import BeautifulSoup
def get_web(url):
	web = requests.get(url)
	if web.status_code == 200:
		return web.text
	else :
		print('傳入網址有錯哦! url: ', web.url)
def get_title(web_content):
	web_content = BeautifulSoup(web_content, 'html5lib')
	div_rows = web_content.find('ul', 'all').find_all('li')
	title_info =[]
	for row in div_rows:
		title = row.find('div','aht_title').a.text.strip()
		rank = row.find('div', 'aht_title_num').span.text.strip()
		title_info.append({
			'rank': rank,
			'title': title
		})
	return title_info
def get_title2(web_content2):
	web_content2 = BeautifulSoup(web_content2, 'html5lib')
	box_title_rows = web_content2.find('div','listphoto boxTitle').find_all('a')
	box_title_list =[]
	for row in box_title_rows:
		box_title = row.text.strip()
		box_title_list.append(box_title)
	# 小新聞列表
	news_rows = web_content2.find('ul','list imm').find_all('li')
	news_list =[]
	for row in news_rows:
		if row.find('a','tit'):
			news_title = row.find('a','tit').p.text.strip()
		if news_title not in news_list:
			news_list.append(news_title)
	return box_title_list, news_list
def print_ans(apple_list):
	print('蘋果頭條:')
	for row in apple_list:
		print('Rank: %s , Title: %s' %(row['rank'], row['title']))
def main():
	apple_url = 'https://tw.appledaily.com/hot/daily'
	web_content = get_web(apple_url)
	title_info = get_title(web_content)
	print_ans(title_info)
	free_url = 'https://news.ltn.com.tw/list/breakingnews/'
	web_content2 = get_web(free_url)
	box_title_list, news_list = get_title2(web_content2)
	print('自由時報大頭條:')
	for row in box_title_list:
		print('Box_title: %s'% row)
	print('自由時報小列表:')
	count = 0
	for row in news_list:
		count+=1
		print('第 %d 條: %s'% (count,row))
if __name__ == '__main__':
	main()