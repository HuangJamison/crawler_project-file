import requests
from bs4 import BeautifulSoup
import time,datetime
import re
import json

ptt_url = 'https://www.ptt.cc'
def get_page(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
	cookies = {'over18': '1'}
	web = requests.get(url, headers = headers, cookies = cookies)
	if web.status_code == 200:
		return web.text
	else:
		print("Invalid url:%s, and the status_code is: %s"% (web.url,web.status_code))
def get_article(dom, date):  #dom為傳回之文字要轉為html, date為今日日期
	web_content = BeautifulSoup(dom, 'html5lib')
	div_a = web_content.find('div',class_='btn-group btn-group-paging').find_all('a')[1]
	pre_page = div_a['href'] #得到上一頁連結
	articles = []
	div_information = web_content.find_all('div', class_='r-ent')
	for div in div_information:
		this_article_date = div.find('div','date').text.strip()
		if this_article_date == date:
			if div.find('div','title').a:  # 排除已刪文情況
				this_title = div.find('div','title').text.strip()
				this_article_url = div.find('div','title').a['href'].strip()
				this_push = div.find('div','nrec').text.strip()
				this_author = div.find('div','author').text.strip()
				if this_push:  #處理推文如果不是數字情況
					try: this_push = int(this_push)  #數字
					except ValueError:
						if this_push == '爆':
							this_push = 99
						elif this_push.startswith('X'):
							this_push = -10
						else:
							this_push = 0
				else:
					this_push = 0
				articles.append({
					'title':this_title,
					'href' :this_article_url,
					'author':this_author,
					'push_num':this_push
				})
	return articles, pre_page
def gossip_articles(current_page, date, threshold):
	if current_page:  #只要有資訊
		articles = []  #今天or昨天文章
		current_articles, pre_page = get_article(current_page, date)
		while current_articles: #只要其有值
			articles += current_articles
			current_page = get_page(ptt_url+pre_page)
			current_articles, pre_page = get_article(current_page, date)
	print('%s 號共: %d 幾篇文章' % (str(date),len(articles)))
	over_target = 0
	for row in articles:
		if row['push_num'] >= threshold:
			print('主題:%s , 作者: %s , 推文數: %s' % (row['title'], row['author'], row['push_num']))
			over_target += 1
	print('%s 號超過 %d 的推文有 %d篇 ' % (str(date), threshold, over_target))
	return pre_page, articles
def get_author(articles, search_word): # 做出可查詢id含有5566字眼的author
	id_count = 0
	for row in articles:
		author = row['author']
		pattern = re.compile(r'\w*'+search_word+'\w*')
		if re.match(pattern, author):
			print('主題:%s , 作者: %s , 推文數: %s' % (row['title'], row['author'], row['push_num']))
			id_count += 1
	print('含 %s 字眼的author，共 %d 個人' %(search_word,id_count))
def main():
	current_page = get_page(ptt_url+ '/bbs/Gossiping/index.html') #取得網頁.text
	today = time.strftime('%m/%d').lstrip('0')  #取得今日日期
	threshold = int(input('篩選推文條件為:  ').strip())
	pre_page, articles = gossip_articles(current_page, today, threshold)  #作articles list輸出
	with open('gossip_today.json', 'w', encoding= 'utf-8') as f:
		json.dump(articles, f, indent= 3, sort_keys=True, ensure_ascii=False)
	search_word = input('輸入要篩選的作者:  ').strip()
	get_author(articles, search_word) #含5566 字眼的作者有幾個
	yesterday = datetime.date.today() - datetime.timedelta(1)
	yesterday = yesterday.strftime('%m/%d').lstrip('0')
	current_page = get_page(ptt_url + pre_page)
	pre_page, articles = gossip_articles(current_page, yesterday, threshold)
	with open('gossip_yesterday.json', 'w', encoding= 'utf-8') as f:
		json.dump(articles, f, indent= 3, sort_keys=True, ensure_ascii=False)
	get_author(articles, search_word) #含5566 字眼的作者有幾個

if __name__ == '__main__':
	main()