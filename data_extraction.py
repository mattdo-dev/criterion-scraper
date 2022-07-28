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

    csv_in = pd.DataFrame(columns=['person', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])

    if os.path.exists(os.path.join(cwd, 'offline_links')):
        for html in os.listdir(os.path.join(cwd, 'offline_links')):
            with open(os.path.join(cwd, 'offline_links', '93.html'), 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                test = soup.find('article').get_attribute_list('data-article-title')
                csv_in['person'] = str(test).replace('’s Top 10', '')[2:-2]
                for index in soup.find_all('p', attrs={'class': 'count'}):
                    i = re.search(r'(10|[1-9])', index.text, re.MULTILINE)
                    if i is not None:
                        print(i.group(0))
                        titles = BeautifulSoup(str(index.next_sibling.next_sibling), 'html.parser')
                        print(index.next_sibling.next_sibling)
                        print(titles.find_all('h3', attrs={'class': 'editorial-film-listitem__title'}))

                break
            break

        csv_in.to_csv('data.csv', sep='^', index=False, mode='w', encoding='utf-8')
    else:
        exit()
