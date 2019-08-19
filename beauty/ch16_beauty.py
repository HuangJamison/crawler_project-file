import requests
from bs4 import BeautifulSoup
import time,datetime
import re, os,urllib.request
import json

ptt_url = 'https://www.ptt.cc'
def get_page(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
	cookies = {'over18': '1'}
	web = requests.get(url, headers=headers, cookies=cookies)
	if web.status_code == 200:
		return web.text
	else:
		return None
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
def beauty_articles(current_page, date, threshold):
	if current_page:  #只要有資訊
		articles = []  #今天or昨天文章
		current_articles, pre_page = get_article(current_page, date)
		print(pre_page)
		while current_articles: #只要其有值
			articles += current_articles
			current_page = get_page(ptt_url+pre_page)
			current_articles, pre_page = get_article(current_page, date)
	print('%s 號共: %d 幾篇文章' % (str(date),len(articles)))
	over_target = 0
	criteria_push_num = []
	for row in articles:
		if row['push_num'] >= threshold:
			print('主題:%s , 作者: %s , 推文數: %s' % (row['title'], row['author'], row['push_num']))
			over_target += 1
			criteria_push_num.append(row)
	print('%s 號超過 %d 的推文有 %d篇 ' % (str(date), threshold, over_target))
	return pre_page, articles,criteria_push_num
def download_image(list_criteria):  #負責把符合推文標準的超連結圖片印出
	# count =0
	for row in list_criteria:
		href = row['href']
		url = ptt_url + href
		page = get_page(url)
		img_list = [] #只存取該網頁的圖片網址
		if page:
			soup = BeautifulSoup(page,'html.parser')
			article_img = soup.find('div','bbs-screen bbs-content',id='main-content').find_all('a')
			title = row['title'].strip()
			for art in article_img:
				img_url = art.text
				pattern = r'https?://(i.)?(m.)?imgur.com'
				if re.match(pattern,img_url):
					img_list.append(img_url)
			save_img(img_list, title)
			# print(row['title'],'有 %d 張圖'%len(img_list))
			# count+=1
	# print('共有 %d篇可以成功抓到網址'%count)
def save_img(img_list, title):
	if img_list: #不是空的
		try:
			os.makedirs(title)
			for img in img_list:
				if img.split('//')[1].startswith('m.'):
					img = img.replace('//m.', '//i.')
				if not img.split('//')[1].startswith('i.'):
					img = img.split('//')[0] + '//i.' + img.split('//')[1]
				if not img.endswith('.jpg'):
					img += '.jpg'
				file_name = img.split('/')[-1]
				urllib.request.urlretrieve(img, os.path.join(title,file_name))
		except Exception as e:
			print(e)

def main():
	current_page = get_page(ptt_url+ '/bbs/Beauty/index.html') #表特版取得網頁.text
	today = time.strftime('%m/%d').lstrip('0')  #取得今日日期
	threshold = int(input('篩選推文條件為:  ').strip())
	pre_page, articles,criteria_push_num = beauty_articles(current_page, today, threshold)  #作articles list輸出
	download_image(criteria_push_num)
	with open('beauty_today.json', 'w', encoding= 'utf-8') as f:
		json.dump(criteria_push_num, f, indent= 3, sort_keys=True, ensure_ascii=False)
	# yesterday = datetime.date.today() - datetime.timedelta(1)
	# yesterday = yesterday.strftime('%m/%d').lstrip('0')
	# current_page = get_page(ptt_url + pre_page)
	# pre_page, articles = gossip_articles(current_page, yesterday, threshold)
	# with open('gossip_yesterday.json', 'w', encoding= 'utf-8') as f:
	# 	json.dump(articles, f, indent= 3, sort_keys=True, ensure_ascii=False)

if __name__ == '__main__':
	main()