import requests
from bs4 import BeautifulSoup
import re # re是regular expression的簡寫package包
def main():
	url = "http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html"
	web = requests.get(url)  #要記得寫get
	if web.status_code == 200:
		web_content = BeautifulSoup(web.text, "html.parser")
		# 任務一:要找出所有含有 "h tag"的文字
		# data_rows = web_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) #法一 找這幾個標籤
		# 法二 用regular expression去抓，更為方便
		# data_rows =  web_content.find_all(re.compile('h[1-6]'))
		# for data in data_rows:
		# 	print(data.text.strip())

		# 任務二:要找出所有以.png結尾並有beginner的png圖檔文字
		# 法一: 先用簡單的find_all 比較笨的寫法
		# png_rows = web_content.find_all('img')
		# print(png_rows)
		# for png in png_rows:
		# 	if ('beginner' in png['src']) and (png['src'].endswith('.png')):  #確認每一個row 最後結尾為.png就印出來
		# 		print(png['src'])
		# 法二: 用re.compile 做做看.png與含有beginner結尾
		# re.compile可以處理更多字元規則,以下用字典方式{}查找 re.compile , 因'.'為特殊以\表示 $代表結束
		# re.compile  .為任何字串
		# png_rows = web_content.find_all('img',{'src' : re.compile("beginner.*\.png$")})
		# for png in png_rows:
		# 	print(png['src'])
		# # 任務三:找尋網址
		# web_div = web_content.find_all('div', class_= 'card-image')
		# url_list =[]
		# pattern = re.compile('http.*://[A-Za-z0-9\.]+')
		# for ur in web_div:
		# 	each_url = ur.a['href']
		# 	if re.match(pattern, each_url):
		# 		url_list.append(each_url)
		# print(url_list)




if __name__ == '__main__':
	main()