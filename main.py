import requests
import bs4
from fake_headers import Headers
import re
from time import sleep

headers = Headers(browser='chrome', os='windows').generate()

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = "https://habr.com/ru/articles/"

response = requests.get(url, headers=headers)

# Функция для поиска слов из списка в тексте
def find_word(KEYWORDS,text):
    for word in KEYWORDS:
            pattern =fr'.*({word}).*'
            result = re.findall(pattern,text, re.I)
            if result:
                return True

if response.status_code == 200:
    soup = bs4.BeautifulSoup(response.text, features='lxml')

    articles_list = soup.select('article.tm-articles-list__item')
    for article in articles_list:
        sleep(2)
        add_= False
        article_head = article.select_one('h2').text
        add_=find_word(KEYWORDS,article_head)
        article_time = article.select_one('time')['title']
        article_text = ''
        article_preview_div = article.select('p')
        link = 'https://habr.com' + article.select_one('a.tm-article-snippet__readmore')['href']
        for art in article_preview_div:
            add_= find_word(KEYWORDS,art.text )
        if add_:
            print(f'<{article_time}> - <{article_head}> - <{link}>')

else:
    print('Страница не найдена')