import requests
import re
from bs4 import BeautifulSoup

def main():
	url = "http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html"
	web = requests.get(url)
	if web.status_code == 200:
		web_content = BeautifulSoup(web.text, 'html.parser')
	# 作業6-1
	title_rows = web_content.find_all('h4', class_= 'card-title')
	article_num = 0 #計算篇數
	for row in title_rows:
		title = row.a.text
		# pattern = re.compile('http*://[a-zA-Z0-9\.]+') #網址是否符合格式
		if len(title) > 0:  #用title 去分
			article_num +=1
	print('此部落格總共 %d 篇文章' %article_num)
	# 作業6-2
	text_rows = web_content.find_all('div', class_= 'card-image')
	crawler_num = 0
	for row in text_rows:
		png = row.img['src']
		pattern_crawler = re.compile('crawler*.\.png$')
		if re.search(pattern_crawler, png):
			crawler_num +=1
	print('含有crawler字眼的png檔有 %d 個' % crawler_num)
	# ch6 作業6-3
	url2 = "http://blog.castman.net/web-crawler-tutorial/ch2/table/table.html"
	web2 = requests.get(url2)
	class_num = 0
	if web.status_code == 200:
		web_content2 = BeautifulSoup(web2.text, 'html.parser')
		tr_rows = web_content2.find('table', class_= 'table').tbody.find_all('tr')
		table_list = []
		for row in tr_rows:
			title_table = row.find_all('td')[0].text
			table_list.append(title_table)
		for i in table_list:
			if len(i) > 0:
				class_num+=1
	print("網站內共有 %d 個課程" % class_num)



if __name__ == '__main__':
	main()

