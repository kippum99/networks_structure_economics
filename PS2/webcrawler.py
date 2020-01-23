from fetcher3 import fetch_links

pageCount = 0
queue = []

def bfs(url):
    global pageCount, queue

    pageCount += 1
    links = [link for link in fetch_links(url) if '.caltech.edu' in link]
    print(links)

bfs('http://www.caltech.edu')
