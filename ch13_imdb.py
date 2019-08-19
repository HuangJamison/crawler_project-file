import requests
from bs4 import BeautifulSoup
import time,datetime
import re
import json,math
from collections import Counter
# cf8db8fc
API_KEY = 'cf8db8fc'
OMDB_URL = 'http://www.omdbapi.com/?apikey=' + API_KEY
def get_data(url):
	data = json.loads(requests.get(url).text)  #json.load
	if data:
		return data
	else:
		return None
def search_keyword(key_word):
	movie_id = []
	query = '+'.join(key_word.split(' ')) #空格用+號代替
	# replace = key_word.replace(' ','+')  print(replace)
	url = OMDB_URL + '&s='+ query
	data = get_data(url)
	if data:
		for row in data['Search']:
			# title = row['Title']
			# year = row['Year']
			ID = row['imdbID']
			movie_id.append(ID)
		total = int(data['totalResults'])
		pages = math.ceil(total/10) #無條件進位
		#取第二頁以後資料
		for i in range(2,pages+1):
			url = OMDB_URL +'&s='+ query+'&page='+ str(i)
			data = get_data(url)
			if data:
				for row in data['Search']:
					ID = row['imdbID']
					movie_id.append(ID)
	'''
	{'Search': [{'Title': 'The Fast and the Furious', 'Year': '2001', 'imdbID': 'tt0232500', 
				'Type': 'movie', 'Poster': ''},
	'''
	return movie_id
def search_id(movie_id):
	url = OMDB_URL + '&i='
	movie_info =[]
	rating_list =[]
	year_list =[]
	for m_id in movie_id:
		data = get_data(url+m_id)
		if data:
			title = data['Title']
			year = data['Year']
			rating = data['imdbRating']
			year_list.append(year)
			movie_info.append({
				'title':title,
				'rating':rating,
				'year':year
			})
	for row in movie_info:
		if row['rating'] != 'N/A':
			rating_list.append(float(row['rating']))

	return movie_info,rating_list,year_list
def main():
	key_word = input('請輸入你想搜尋的電影名稱(英文):')
	movie_id = search_keyword(key_word)
	movie_info,rating_list,year_list= search_id(movie_id)
	year_dict = Counter(year_list)  #練習用counter輸出
	print('您輸入的key_word: %s,共有 %d 個結果' %(key_word, len(movie_info)))
	print(year_dict)
	print('您輸入的key_word: %s \n平均imdb_rating: %.2f' %(key_word, sum(rating_list)/len(rating_list)))

if __name__ == '__main__':
	main()