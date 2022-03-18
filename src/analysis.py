import requests
from config_parse import get_path

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 ',
}


def get_m3u8(url: str):
    response = requests.get(url=url, headers=headers, timeout=15)
    with open(get_path()+'/cache/cache.m3u8', 'wb') as writer:
        writer.write(response.content)



