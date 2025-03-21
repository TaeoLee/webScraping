from urllib.request import Request,urlopen

url= "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
req = Request(url, headers=headers)


page = urlopen(req)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)