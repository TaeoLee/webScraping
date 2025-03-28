import requests
from bs4 import BeautifulSoup

url = "https://kr.investing.com/indices/us-spx-500-futures?cid=1175153"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Use the data-test attribute to find the div
price_div = soup.find('div', {'data-test': 'instrument-price-last'})

if price_div:
  print("Price:", price_div.text.strip())
else:
  print("Price not found.")
