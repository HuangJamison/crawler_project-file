import re,json
import requests
from bs4 import BeautifulSoup
def get_web(url):
	web = requests.get(url)
	if web.status_code ==200:
		return web.text
	else:
		print("有錯哦! Valid: ", web.url)
def main():
	url = 'https://tw.dictionary.search.yahoo.com/search?p=hot'
if __name__ == '__main__':
	main()