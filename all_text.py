import requests
import bs4
from fake_headers import Headers
import re
from main import find_word
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
        add_= False
        article_head = article.select_one('h2').text
        add_=find_word(KEYWORDS,article_head)
        article_time = article.select_one('time')['title']
        link = 'https://habr.com' + article.select_one('a.tm-article-snippet__readmore')['href']
        url_art = link
        response_1 = requests.get(url_art, headers=headers)
        if response_1.status_code == 200:
                soup_1 = bs4.BeautifulSoup(response_1.text, features='lxml')
                page_body = soup_1.select_one('div.article-body')
                art_body_text = page_body.select('p')
                for items in art_body_text: 
                    add_=find_word(KEYWORDS,items.text)
        sleep(2)       
        if add_:
            print(f'<{article_time}> - <{article_head}> - <{link}>')

else:
    print('Страница не найдена')

                