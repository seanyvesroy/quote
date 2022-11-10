
import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
page = requests.get('https://www.goodreads.com/quotes/tag/fantasy-fiction#:~:text=%E2%80%9COne%20day%2C%20you%20will%20be,to%20start%20reading%20fairytales%20again.%E2%80%9D&text=%E2%80%9CWhen%20people%20dis%20fantasy%E2%80%94mainstream,Tolkien%2C%20and%20Tolkien\'s%20innumerable%20heirs.', headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
