import os
import urllib.request

if __name__ == "__main__":
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, 'offline_links')):
        os.makedirs(os.path.join(cwd, 'offline_links'))

    offline_links = os.path.join(cwd, 'offline_links')

    if os.path.exists(os.path.join(cwd, 'links.txt')):
        with open(os.path.join(cwd, 'links.txt'), 'r', encoding='utf-8') as f:
            i = 0
            for url in f:
                print(url)
                req = urllib.request.Request(url, headers={'User-Agent': 'Chrome/41.0.2228.0'})
                with urllib.request.urlopen(req) as response:
                    html = response.read()
                    with open(os.path.join(offline_links, f'{str(i)}.html'), 'w', encoding='utf-8') as f2:
                        f2.write(str(html))
                        f2.close()
                i += 1

            f.close()
