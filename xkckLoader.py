#!/usr/bin/env python3
# xkcdLoader.py - Downloads every single XKCD comic into a directory

import requests
import argparse
import os
import bs4
import time
import threading


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

    # Startd multiple download threads
    download_threads = []
    for i in range(0, 1400, 100):
        download_thread = threading.Thread(target=download_xkcd,
                                           args=(i, i + 99,
                                                 base_url,
                                                 target_dir))
        download_threads.append(download_thread)
        download_thread.start()

    # Wat for all threads to end
    for download_thread in download_threads:
        download_thread.join()
    print('Done.')


def download_xkcd(start_comic, end_comic, base_url, target_dir):
    for url_number in range(start_comic, end_comic):
        soup = load_page(os.path.join(base_url, str(url_number)))
        save_img(soup, target_dir)


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


if __name__ == '__main__':
    main(BASE_URL)
