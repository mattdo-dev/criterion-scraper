import os

from html.parser import HTMLParser


class LinksParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        """
        This method is called when a <a> start tag is found.
        Specifically, we are looking for the <a> tags that have the class attrs:
            pk-c-tout__media pk-c-tout__media--small

        The links should look as such:
            https://www.criterion.com/current/top-10-lists/348-ali-abbasi-s-top-10

        :param tag:
        :param attrs:
        :return:
        """
        if tag == 'a' and attrs[0][1] == 'pk-c-tout__media pk-c-tout__media--small':
            self.links.append(dict(attrs).get('href'))

    def get_links(self):
        return self.links


if __name__ == '__main__':
    html_file = os.path.join(os.path.dirname(__file__), 'top10.html')
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
            parser = LinksParser()
            parser.feed(html)
            links = parser.get_links()
            print(links)
            print(len(links))
            f.close()
