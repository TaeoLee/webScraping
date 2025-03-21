from urllib.request import urlopen

url= "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)