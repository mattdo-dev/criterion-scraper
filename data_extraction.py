import os
import pandas
import re

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

if __name__ == "__main__":
    cwd = os.getcwd()

    if os.path.exists(os.path.join(cwd, 'offline_links')):
        for html in os.listdir(os.path.join(cwd, 'offline_links')):
            with open(os.path.join(cwd, 'offline_links', html), 'r', encoding='utf-8') as f:
                html = f.read()
                print(re.search(list_regex, html).group(2))
                break
    else:
        exit()
