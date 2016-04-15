import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

textToSearch = 'hello world'
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
url_list = []
with urllib.request.urlopen(url) as response:
    the_page = response.read()
    soup = BeautifulSoup(the_page, "html.parser")
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        url_final = 'https://www.youtube.com' + vid['href']
        test = url_final.split()
        url_list.append(test)
        # print(test)
    print(url_list[0])
