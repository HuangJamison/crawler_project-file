import requests
from bs4 import BeautifulSoup
def main():
	url = "http://blog.castman.net/web-crawler-tutorial/ch2/table/table.html"
	web = requests.get(url)
	if web.status_code == 200:
		web_tag = BeautifulSoup(web.text, 'html.parser')
		price = []
		#先找table 底下 tbody內找所有tr的部分
		web_table = web_tag.find('table', class_= 'table').tbody.find_all('tr')
		for row in web_table:
			each_price = row.find_all('td')[2].text #因td內第三個內容
			price.append(int(each_price))
		print("sum:",sum(price))
		print("avg:",sum(price)/len(price))
main()


