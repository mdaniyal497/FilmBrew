import requests
from bs4 import BeautifulSoup
import re


def get_image(tconst):

    url = "https://www.imdb.com/title/" + tconst

    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    # find all with the image tag
    images = data.find_all('img', src=True)
    image_src = [x['src'] for x in images]
    # select only jp format images
    image_src = [x for x in image_src if x.endswith('.jpg')]

    return image_src[0]


def get_summary(tconst):

    url = "https://www.imdb.com/title/" + tconst

    html = requests.get(url).content
    unicode_str = html.decode("utf8")
    encoded_str = unicode_str.encode("ascii", 'ignore')
    news_soup = BeautifulSoup(encoded_str, "html.parser")
    a_text = news_soup.find_all("div", {"class": "summary_text"})
    y = [re.sub(r'<.+?>', r'', str(a)) for a in a_text]

    return y[0].strip()
