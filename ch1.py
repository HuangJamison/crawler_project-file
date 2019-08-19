import requests
from bs4 import BeautifulSoup  # 網頁結構格式套件
# 擷取網頁資訊  200 為好的 404為找不到
def main():
    h1 = get_url("http://blog.castman.net/py-scraping-analysis-book/ch1/connect.html","h1")
    print("標題文字:",h1)
    p = get_url("http://blog.castman.net/py-scraping-analysis-book/ch1/connect.html","p")
    print("段落文字:",p)
    button = get_url("http://blog.castman.net/py-scraping-analysis-book/ch1/connect.html","button")
    print("button:",button)
def get_url(url, tag):
    try:
        web = requests.get(url)
        if web.status_code == 200: #代表正常執行
            data = BeautifulSoup(web.text, 'html.parser')  # 以bfs去獲取此html格式資料
            title = data.find(tag)
            return title.text
    except Exception:
        return "不存在哦!!"
main()