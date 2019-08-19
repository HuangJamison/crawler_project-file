from bs4 import BeautifulSoup
import requests
import re,urllib.parse
import json,csv
def get_web(url):
	web = requests.get(url)
	if web.status_code == 200:
		return web.text
	else:
		print('傳入網址有誤,網址:',url.web)
def print_ans(arr):
	for row in arr:
		print(row)
def main():
	url = 'https://ezprice.com.tw/s/'
	word  = 'oppo reno 紫色'
	# 用urllib.parse 做html encoding
	search_word = urllib.parse.quote(word)
	search_url = url+ search_word+'/'
	web = get_web(search_url)
	web_content = BeautifulSoup(web, 'html5lib')
	# dict_search ={'name':[],'price':[],'platform':[]}
	list_search = []
	div_rows = web_content.find_all('div','search-rst clearfix')
	for row in div_rows:
		if row.find('h2','pd-name').text.strip():
			name = row.find('h2','pd-name').text.strip()
		else:
			name = '無資訊'
		if row.find('span','num').text.strip():
			price = row.find('span','num').text.strip()
		else:
			price = '無'
		if row.find('span','platform-name').text.strip():
			platform = row.find('span', 'platform-name').text.strip()
		else:
			platform = '無'
		#整理上述資訊於List 裝 dict
		# dict_search['name'].append(name)
		# dict_search['price'].append(int(price))
		# dict_search['platform'].append(platform)
		list_search.append({
			'name':name,
			'price':int(price),
			'platform':platform,
		})
	print('共有 %d 筆的搜尋資料'% len(list_search))
	list_search.sort(key=lambda k: (k.get('price', 0)), reverse=True)
	print_ans(list_search)
	with open('ezprice.csv','w',encoding = 'utf-8',newline='') as f:
		writer = csv.writer(f)
		writer.writerow(list_search[0].keys())
		for row in list_search:
			writer.writerow(row.values())
		# writer.writeheader(dict_search.keys())
		# rows = zip(*dict_search.values())
		# for row in rows:
		# 	writer.writerow(row)
		# 	print(row)
	list1=[['a','b','c'],[1,2,3]]
	rows= zip(*list1)
	for row in rows:
		print(row)
if __name__ == '__main__':
	main()