import requests
from bs4 import BeautifulSoup
import json
def get_web(url):
	web = requests.get(url)
	if web.status_code ==200:
		return web.text
	else:
		return None
def main():
	url = 'https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx'
	web = get_web(url)
	web_content = BeautifulSoup(web,'lxml')
	viewstate = web_content.find('input')['value'].strip()
	viewstagegen = web_content.find('input',id ='__VIEWSTATEGENERATOR')['value'].strip()
	eventvad = web_content.find('input',id = '__EVENTVALIDATION')['value'].strip()
	data = {
		'__VIEWSTATE':viewstate,
		'__VIEWSTATEGENERATOR':viewstagegen,
		'__EVENTVALIDATION':eventvad,
		'ctl05$lbSite': '44',
		'ctl05$lbParam':'4',
		'ctl05$txtDateS':'2019/08/12',
		'ctl05$txtDateE':'2019/08/14',
		'ctl05$btnQuery':'查詢即時值'
	}
	web = requests.post(url, data = data)
	new_web_content = BeautifulSoup(web.text, 'xml')
	table_rows = new_web_content.find('table','TABLE_G').find_all('tr',style='color:Black;')
	for row in table_rows:
		rows_in = row.find_all('td')
		for row2 in rows_in:
			print(row2.text,end=' ')
		print()
def youtube():
	url = "https://www.youtube.com/feed/trending/"

	request = requests.get(url)
	content = request.content
	soup = BeautifulSoup(content, "html.parser")

	container = soup.select("h3 a")
	hot_rows = soup.select('div.yt-lockup-meta')
	# print(type(container))
	# print(container)
	for item,row in zip(container,hot_rows):
		if item and row:
			print(item.text.strip(),row.text.strip())
if __name__ == '__main__':
	# main()
	youtube()