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

    cols = ['person', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

    csv_in = pd.DataFrame(columns=cols)

    if os.path.exists(os.path.join(cwd, 'offline_links')):
        html_files = os.listdir(os.path.join(cwd, 'offline_links'))
        html_files_len = len(html_files)

        person = [] * html_files_len
        a1 = [] * html_files_len
        a2 = [] * html_files_len
        a3 = [] * html_files_len
        a4 = [] * html_files_len
        a5 = [] * html_files_len
        a6 = [] * html_files_len
        a7 = [] * html_files_len
        a8 = [] * html_files_len
        a9 = [] * html_files_len
        a10 = [] * html_files_len
        a11 = [] * html_files_len
        a12 = [] * html_files_len
        a13 = [] * html_files_len
        a14 = [] * html_files_len
        a15 = [] * html_files_len
        a16 = [] * html_files_len

        for i in range(0, len(html_files) + 1):
            with open(os.path.join(cwd, 'offline_links', html_files[i]), 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                test = soup.find('article').get_attribute_list('data-article-title')
                person[i] = str(test).replace('’s Top 10', '')[2:-2]
                col = None
                films = ""
                for index in soup.find_all('p', attrs={'class': 'count'}):
                    titles = BeautifulSoup(str(index.next_sibling.next_sibling), 'html.parser')
                    col = index.text.replace("(tie)", "").replace(" ", "")
                    if index.text != ' ':
                        if col == '1':
                            a1[i] = films
                        films: str = titles.find('h3', attrs={'class': 'editorial-film-listitem__title'}).text
                    elif index.text == ' ':
                        films: str = films + '|' + titles.find('h3',
                                                               attrs={'class': 'editorial-film-listitem__title'}).text

        for html in os.listdir(os.path.join(cwd, 'offline_links')):
            with open(os.path.join(cwd, 'offline_links', html), 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                test = soup.find('article').get_attribute_list('data-article-title')
                person.append(str(test).replace('’s Top 10', '')[2:-2])
                col = None
                films = ""
                for index in soup.find_all('p', attrs={'class': 'count'}):
                    titles = BeautifulSoup(str(index.next_sibling.next_sibling), 'html.parser')
                    col = index.text.replace("(tie)", "").replace(" ", "")
                    if index.text != ' ':
                        if col == '1':
                            a1.append(films)
                        elif col == '2':
                            a2.append(films)
                        elif col == '3':
                            a3.append(films)
                        elif col == '4':
                            a4.append(films)
                        elif col == '5':
                            a5.append(films)
                        elif col == '6':
                            a6.append(films)
                        elif col == '7':
                            a7.append(films)
                        elif col == '8':
                            a8.append(films)
                        elif col == '9':
                            a9.append(films)
                        elif col == '10':
                            a10.append(films)
                        elif col == '11':
                            a11.append(films)
                        elif col == '12':
                            a12.append(films)
                        elif col == '13':
                            a13.append(films)
                        elif col == '14':
                            a14.append(films)
                        elif col == '15':
                            a15.append(films)
                        films: str = titles.find('h3', attrs={'class': 'editorial-film-listitem__title'}).text
                    elif index.text == ' ':
                        films: str = films + '|' + titles.find('h3',
                                                               attrs={'class': 'editorial-film-listitem__title'}).text

        csv_in['person'] = pd.Series(person)
        csv_in['1'] = pd.Series(a1)
        csv_in['2'] = pd.Series(a2)
        csv_in['3'] = pd.Series(a3)
        csv_in['4'] = pd.Series(a4)
        csv_in['5'] = pd.Series(a5)
        csv_in['6'] = pd.Series(a6)
        csv_in['7'] = pd.Series(a7)
        csv_in['8'] = pd.Series(a8)
        csv_in['9'] = pd.Series(a9)
        csv_in['10'] = pd.Series(a10)
        csv_in['11'] = pd.Series(a11)
        csv_in['12'] = pd.Series(a12)
        csv_in['13'] = pd.Series(a13)
        csv_in['14'] = pd.Series(a14)
        csv_in['15'] = pd.Series(a15)
        csv_in['16'] = pd.Series(a16)

        csv_in.to_csv('data.csv', sep=';', index=False, mode='w', encoding='utf-8')
    else:
        exit()
