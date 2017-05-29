#!/usr/bin/env python3
# xkcdLoader.py - Downloads every single XKCD comic into a directory

import requests
import argparse
import os
import bs4
import time


BASE_URL = 'http://xkcd.com'
MAX_RETRIES = 3


def main(base_url):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        help='Specifies a target directory to save images to')
    args = parser.parse_args()

    target_dir = 'xkcd'

    if args.dir:
        target_dir = args.dir

    os.makedirs(target_dir, exist_ok=True)
    url = base_url

    while not url.endswith('#'):
        soup = load_page(url)
        save_img(soup, target_dir)
        url = next_img_url(soup)

    print('Done.')


def load_page(url, retry_count=0):
    try:
        print('Loading page {0}'.format(url))
        res = requests.get(url)
        res.raise_for_status()

        return bs4.BeautifulSoup(res.text, 'html.parser')
    except ConnectionResetError as e:
        if retry_count == MAX_RETRIES:
            raise e
        print('Connection got reset. Trying again...')
        time.sleep(0.5)
        load_page(url, retry_count + 1)


def save_img(soup, target_dir):
    comic_elem = soup.select('#comic img')

    if comic_elem == []:
        print('Could not find comic image.')
    else:
        comic_url = 'http:{0}'.format(comic_elem[0].get('src'))
        file_path = os.path.join(target_dir, os.path.basename(comic_url))

        if os.path.exists(file_path):
            print('Image exists. Skipping file...')
        else:
            print('Downloading image {0}'.format(comic_url))
            res = requests.get(comic_url)
            res.raise_for_status()

            image_file = open(os.path.join(target_dir,
                                           os.path.basename(comic_url)), 'wb')
            for chunk in res.iter_content(100000):
                image_file.write(chunk)
            image_file.close()


def next_img_url(soup):
    prev_link = soup.select('a[rel="prev"]')[0]
    link_source = prev_link.get('href')
    return 'http://xkcd.com{0}'.format(link_source)


if __name__ == '__main__':
    main(BASE_URL)
