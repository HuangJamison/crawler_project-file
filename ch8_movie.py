import requests
import re,json,numpy,pandas
from bs4 import BeautifulSoup
def get_pages(url):
	web = requests.get(url)
	if web.status_code == 200:
		return web.text
	else:
		print('輸入網址有錯哦! Invalid url:', web.url)
def print_ans(movie_list):
	print('依照滿意度最高排序本週新電影:')
	for row in movie_list:
		print('movie name: %s EN:[%s], movie time: %s, movie satisfy: %s'
		      %(row['movie_name'],row['movie_name_en'],row['movie_time'],row['movie_satisfy']))
def get_movie(dom):
	web_content= BeautifulSoup(dom, 'html5lib')
	div_movie = web_content.find_all('div', class_= 'release_info_text')
	movie_info=[]
	for row in div_movie:
		movie_name = row.find('div', 'release_movie_name').a.text.strip()
		movie_name_en = row.find('div', 'en').a.text.strip()
		movie_time = get_date(row.find('div', 'release_movie_time').text.strip())
		movie_satisfy = float(row.find('div', 'leveltext starwithnum').span['data-num'].strip())
		movie_id = get_id(row.find('div', 'release_movie_name').a['href'])
		movie_tra = row.find_next_sibling('div','release_btn color_btnbox').find_all('a')[1]
		#再整理一次
		movie_tra = movie_tra['href']
		movie_intro = row.find('div','release_text').span.text.strip()
		movie_info.append({
			'movie_name': movie_name,
			'movie_name_en': movie_name_en,
			'movie_time': movie_time,
			'movie_satisfy': movie_satisfy,
			'movie_id':movie_id,
			'movie_intro':movie_intro
		})
		movie_info.sort(key= lambda k: (k.get('movie_satisfy',0),
		                                k.get('movie_time',0)), reverse= True)
		#依照滿意度排序再按照時間排序 reverse=T代表是由大到小
	return movie_info
def get_date(date_str):
	pattern= '\d+-\d+-\d+'
	release_time = re.search(pattern ,date_str)
	return release_time.group(0)
def get_id(id_str):
	id = id_str.split('movieinfo_main')[1].split('-')[-1]
	return id
def main():
	url = 'https://movies.yahoo.com.tw/movie_intheaters.html'
	web_content = get_pages(url)
	movie_info = get_movie(web_content)
	print_ans(movie_info)
	with open('yahoo_movie.json', 'w', encoding= 'utf-8') as f:
		json.dump(movie_info, f, indent= 3, sort_keys=False, ensure_ascii=False)

if __name__ == '__main__':
	main()