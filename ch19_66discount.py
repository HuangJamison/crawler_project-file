from bs4 import BeautifulSoup
import requests
import re,urllib.parse
import json,csv,numpy,pandas

def get_web(url):
	web = requests.get(url)
	# 因為網頁是big-5編碼
	web.encoding = 'big5'
	if web.status_code == 200:
		return web.content
def find_discount(web_content):
	div_rows = web_content.find('div','mod-04 clearfix').find_all('div','table-td')
	book_list=[]
	for row in div_rows:
		book = row.find('h4').text.strip()
		date = row.find('em').text.strip()
		price = row.find('li').b.text.strip()
		book_list.append(book+date+'  價格:'+price)
	print('\n'.join(book_list))
def main():
	url = 'https://activity.books.com.tw/books66/'
	web = get_web(url)
	web_content = BeautifulSoup(web, 'html.parser')
	find_discount(web_content)

if __name__ == '__main__':
	main()