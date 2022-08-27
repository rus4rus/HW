import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent' :	'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept-Language' :	'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
list_of_articles = []

r = requests.get('https://habr.com/ru/all/', headers=HEADERS)
soup = BeautifulSoup(r.text,features='html.parser')
articles = soup.find_all("div", class_='tm-article-snippet')
for article in articles:
    #get title, nick_name, snippets, text preview for searching keywords
    title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').text
    href = 'https://habr.com' + article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').find('a').attrs['href']
    nick_name = article.find(class_="tm-user-info__username").text.strip()
    text_preview = article.find("div", class_='tm-article-body tm-article-snippet__lead').text
    snippets = article.find_all(class_='tm-article-snippet__hubs-item')
    snippets = [snippet.find('a').text.strip('*').strip() for snippet in snippets]
    date = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
    #create array of text to find key words
    common_text = title + nick_name + text_preview + ','.join(snippets)
    words = [common_text.lower().find(word.lower()) for word in KEYWORDS]
    if sum(words) != -len(KEYWORDS):
        keyword_article_dict = {
            'title' : title,
            'href' : href,
            'nick_name' : nick_name,
            'date' : date,
            'snippets' : snippets
        }
        list_of_articles.append(keyword_article_dict)
    else:
        #if don't find keywords - open article and find in it
        r = requests.get(href, headers=HEADERS)
        soup = BeautifulSoup(r.text, features='html.parser')
        article_text = soup.find(class_='tm-article-body').text
        words = [article_text.lower().find(word.lower()) for word in KEYWORDS]
        if sum(words) != -len(KEYWORDS):
            keyword_article_dict = {
                'title': title,
                'href': href,
                'nick_name': nick_name,
                'date': date,
                'snippets': snippets
                }
            list_of_articles.append(keyword_article_dict)
print(f'Список статьей с ключевыми словами: {KEYWORDS}:')
for article in list_of_articles:
    print(f"{article['date']} - {article['title']} - {article['href']}" )