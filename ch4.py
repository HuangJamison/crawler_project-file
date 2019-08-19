import requests
from bs4 import BeautifulSoup
def main ():
	url = "http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html"
	crawler(url)
def crawler(url):
	try:
		web = requests.get(url)
		if web.status_code == 200:
			data = BeautifulSoup(web.text, "html.parser")
			tag_all = data.find_all("div", class_="content")
			for tags in tag_all:
				#第一種
				# print(tags.h6.text.strip(),tags.h4.a.text.strip(),tags.p.text.strip())
				#第二種
				s = []
				for i in tags.stripped_strings:
					s.append(i)
				print(s)
	except Exception:
		web = '沒有資料哦!'
		print(web)
main()




