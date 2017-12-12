#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Unfortunately this codes can extract only the first 80 pages....
#<table class="pager_table"cellspacing="0" summary="ページャー" width="100%">
#	<tr>
#		<td class="t-left t-left_new">
#			<span class="pageLabel">現在表示1～80 / 2318アイテム</span>
######### 多分、上のあたりがネック。JavaScriptを操作する必要あり。
import time    # Controle time span by scraping.
import re    # for Regular Expression (=regexp?
import lxml.html
import requests

def main():
    list_page = 'http://e-comerce.com'
    response = requests.get(list_page)
        # Initial Setup

    item_urls = scrape_list_page(response)
        # Use the function for extracting all detaile-page-url's
        # The extructed list is a generator and inclueds some duplications.
        # http://jutememo.blogspot.jp/2008/07/python-1.html

    item_unique_urls = []
    for x in item_urls:
        if x not in item_unique_urls:
            item_unique_urls.append(x)
    # Thus we need to extruct duplicated urls

    for url in item_unique_urls:
        key = extruct_key(url)
        time.sleep(1)
        response = requests.get(url)
        ec_item = scrape_detail_page(response)
        print(ec_item)

def scrape_list_page(response):
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)

    for a in root.cssselect('a[data-ga-event-category="eec_productlist"]'):
        item_url = a.get('href')
        yield item_url

def scrape_detail_page(response):
    root = lxml.html.fromstring(response.content)
    ec_item = {
        'url': response.url
        , 'key': extruct_key(response.url)
    }
    return ec_item

def extruct_key(url):
    item_id = url[-7:-1]
    return item_id

if __name__ == '__main__':
    main()
