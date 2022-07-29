from html.parser import HTMLParser
from urllib.request import urlopen, Request

to_get = 'https://www.criterion.com/current/top-10-lists'


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
        """
        if tag == 'a' and attrs[0][1] == 'pk-c-tout__media pk-c-tout__media--small':
            self.links.append(dict(attrs).get('href'))

    def get_links(self):
        return self.links


class MoviesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []

    def handle_starttag(self, tag, attrs):
        """
        Luckily for us the criterion website is updated and has consistent HTML formatting for scraping.
        The rest is trivial, besides making sure that all the movie titles are consistent.

        Our list is contained in the <ul> tag with the class attrs:
            editorial-filmlist

        There are 10 list items in the <ul> tag, ranked from 1 to 10.
        The matter now is dealing with ranked ties and formatting for data collection purposes.
        """
        if tag == 'a' and attrs[0][1] == 'pk-c-tout__media pk-c-tout__media--small':
            self.movies.append(dict(attrs).get('href'))

    def get_movies(self):
        return self.movies


def collect_links():
    # req = Request(to_get, headers={'User-Agent': 'Chrome/41.0.2228.0'})
    # with open('top10.html', 'w', encoding='utf-8') as f:
    #     f.write(urlopen(req).read().decode('utf-8'))

    with open('top10.html', 'r', encoding='utf-8') as f:
        html = f.read()
        parser = LinksParser()
        parser.feed(html)
        links = parser.get_links()
        f.close()

    f = open("links.txt", "w")
    for link in links:
        f.write(link + "\n")
    f.close()


if __name__ == "__main__":
    collect_links()
