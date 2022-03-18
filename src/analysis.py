import math
import os

import requests
from config_parse import get_path

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 ',
}


def get_m3u8(url: str):
    response = requests.get(url=url, headers=headers, timeout=15)
    with open(get_path() + '/cache/cache_1.m3u8', 'wb') as writer:
        writer.write(response.content)


def find_url_path(url: str):
    n = len(url) - 1
    while url[n] != '/':
        n = n - 1
    return url[:n]


def analysis_m3u8(url: str):
    split_count: int = 0
    with open(get_path() + '/cache/cache_1.m3u8', 'r') as reader:
        with open(get_path() + '/cache/cache_2.m3u8', 'wb') as writer:
            while True:
                line = reader.readline()
                if not line:
                    return split_count
                elif line[0] == '#':
                    continue
                else:
                    writer.write((find_url_path(url) + '/' + line).encode())
                    split_count = split_count + 1


def download(split_count: int):
    with open(get_path() + '/cache/cache_2.m3u8', 'r') as reader:
        download_count = 0
        while True:
            line = reader.readline()
            if not line:
                print('Download completely!')
                return
            else:
                url = line[:-1]
                download_count = download_count + 1
                response = requests.get(url=url, headers=headers, stream=True, timeout=60)
                with open(get_path() + '/cache/ts_cache' + str(download_count) + '.ts', 'wb') as writer:
                    downloaded = 0
                    total_size = response.headers.get('content-length')
                    total_size = int(total_size)/1024
                    total_size = math.ceil(total_size)
                    print(total_size)
                    for data in response.iter_content(chunk_size=1024):
                        writer.write(data)
                        downloaded = downloaded + 1
                        print('Downloading:' + str(downloaded) + 'KB/'+str(total_size) + 'KB----'+str(download_count) + '/' + str(split_count))


def generate_list(split_count: int):
    count: int = 1
    with open(get_path() + '/cache/cache_3.txt', 'wb') as writer:
        while count <= split_count:
            writer.write(("file '" + get_path() + "/cache/ts_cache" + str(count) + ".ts'\n").encode())
            count = count + 1


def merge(name: str):
    os.system(
        'ffmpeg -f concat -safe 0 -i ' + get_path() + '/cache/cache_3.txt ' + get_path() + '/output/' + name + '.mp4')
    os.system('rm '+get_path()+'/cache/*')
