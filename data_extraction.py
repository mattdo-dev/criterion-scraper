import pandas as pd
import os
import re

from bs4 import BeautifulSoup
from html.parser import HTMLParser


class LinksParser(HTMLParser):
    """
    NOTES:
        editorial-film-listitem__director tussock: DIRECTOR
        editorial-film-listitem__title: TITLE
        editorial-film-listitem__desc: DESCRIPTION
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        """
        Get the ul ranking from the html file.
        """
        if tag == 'ul' and attrs[0][1] == 'editorial-filmlist':
            self.links.append(dict(attrs).get('href'))


list_regex = re.compile(r'<ul class="editorial-filmlist" (data-is-quickshop)?>(.*?)</ul>', re.UNICODE)
title = re.compile(r'<title>(.*?)</title>', re.UNICODE)
director = re.compile(r'<h5 class="editorial-film-listitem__director tussock">(.*?)</h5>', re.UNICODE)
movies = re.compile(r'<h3 class="editorial-film-listitem__title">(.*?)</h3>', re.UNICODE)

if __name__ == "__main__":
    cwd = os.getcwd()

    if not os.path.exists(cwd + '/data.csv'):
        csv_in = pd.DataFrame(columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    else:
        csv_in = pd.read_csv(cwd + '/data.csv', sep='^')
        if list(csv_in.columns) == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            csv_in.drop(columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], inplace=True)

    if os.path.exists(os.path.join(cwd, 'offline_links')):
        for html in os.listdir(os.path.join(cwd, 'offline_links')):
            with open(os.path.join(cwd, 'offline_links', html), 'r', encoding='utf-8') as f:
                html = f.read()
                soup = BeautifulSoup(html, 'html.parser')
                for index in soup.find_all('p', attrs={'class': 'count'}):
                    re.match(r'(1|2|3|4|5|6|7|8|9|10) [3]?', index.text)
                    # print(index.next_sibling.next_sibling)

                # print(re.search(title, html).group(1))
                # print(re.findall(director, html))
                # print(re.findall(movies, html))

            break
        csv_in.to_csv('data.csv', sep='^', index=False, mode='a', encoding='utf-8')
    else:
        exit()
