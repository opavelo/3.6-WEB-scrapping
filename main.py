import requests
from bs4 import BeautifulSoup
from pprint import pprint

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
response = requests.get('https://habr.com/ru/all/')
links = []

if not response.ok:
    raise ValueError('No response')

text = response.text
soup = BeautifulSoup(text, features="html.parser")
articles = soup.find_all('article')

for article in articles:
    for hubs in article.find_all('a', class_='hub-link'):
        hubs = {hubs.text.lower()}
        if KEYWORDS & hubs:
            href = article.find('a', class_="post__title_link").attrs.get('href')
            name = article.find('a', class_="post__title_link").text
            links.append(href)
            print('Совпадение в ТЭГах:', name,":",href)

    href = article.find('a', class_="post__title_link").attrs.get('href')
    if href not in links:
        response = requests.get(href)
        if not response.ok:
            raise ValueError('No response')
        text = response.text
        soup = BeautifulSoup(text, features="html.parser")
        for words in soup.find_all('div', class_="post__body"):
            words = words.text.lower().split()
            words = set(words)
            if KEYWORDS & words:
                name = article.find('a', class_="post__title_link").text
                print('Совпадение в тексте:', name, ":", href)
