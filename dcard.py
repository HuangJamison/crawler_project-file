import requests
import re,time,datetime
from bs4 import BeautifulSoup
import json
def printans(alist):
	print('共%d篇:'%len(alist))
	for i in alist:
		print(i)
def main():
	url = 'https://www.dcard.tw/f'
	user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
	web = requests.get(url, headers = user_agent)
	# 用web.encoding 去查詢編碼原則 utf-8
	if web.status_code ==200 :
		web_content = BeautifulSoup(web.text, 'html.parser')
	# < h3 class ="Title__Text-v196i6-0 kbMFFv" > 你曾經被韓國瑜感動過嗎？ < / h3 >
	div_rows = web_content.find_all('div', re.compile(r'NormalPostLayout__TitleWrapper-sc-\w+'))
	hot_num = 0
	hot_title = []
	for row in div_rows:
		hot_num +=1
		hot_title.append(row.h3.text)
		if hot_num >= 10:
			break
	printans(hot_title)
	# yesterday = datetime.date.today() - datetime.timedelta(1)
	# print(yesterday.strftime('%m/%d').lstrip('0'))
	# author = 'eee1035566aa88'
	# pattern = re.compile(r'\w*5566\w*')
	# if re.match(pattern, author):
	# 	print('y')
	with open('dcard.json', 'w', encoding= 'utf-8') as f:
		json.dump(hot_title, f, indent= 5, sort_keys=True, ensure_ascii= False)
if __name__ == '__main__':
	main()