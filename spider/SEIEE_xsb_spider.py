#!/usr/bin/env python
# coding: utf-8

# spider of SJTU SEIEE xsb

import sys
import os
import re
import requests
from bs4 import BeautifulSoup

def SEIEE_xsb_spider_get_all(dir):
    return SEIEE_xsb_spider(True, dir)

def SEIEE_xsb_spider_get_new(dir):
    return SEIEE_xsb_spider(False, dir)

def SEIEE_xsb_spider(is_get_all, dir):
    _notice_list = []
    for i in range(1, 88):
        url = 'http://xsb.seiee.sjtu.edu.cn/xsb/list/705-' + str(i) + '-20.htm'
        html = get_page_html(url)
        page_url_list = get_page_url_list(html)
        notice_list = download_url(page_url_list, dir, is_get_all)
        for notice in notice_list:
            _notice_list.append(notice)
    return _notice_list

def get_page_html(url):
    try:
        html = requests.get(url, timeout = 10)
    except requests.exceptions.ConnectionError:
        print('[get_page_html]Error: url' + url[0] + 'connect failed!')
        return
    #print(html.encoding)  #查看网页返回的字符集类型
    #print(html.apparent_encoding) #自动判断字符集类型
    html.encoding = html.apparent_encoding
    result = html.text
    return result

def get_page_url_list(html):
    page_url_list = []
    url_list = re.findall(r'href="(/xsb/info/\d*.htm)"', html, re.S)
    html.encode('utf-8')
    title_list = re.findall(r'title="<?b?>?(.*?)<?/?b?>?" target=', html, re.S)
    i = 0
    for url in url_list:
        element = ['http://xsb.seiee.sjtu.edu.cn' + url, title_list[i]]
        page_url_list.append(element)
        #print('[get_page_url_list]find url: ' + page_url_list[i][0] + '  tittle: ' + page_url_list[i][1])
        i = i+1
    return page_url_list


def download_url(url_list, dir, is_cover):
    i = 0
    text_list = []
    new_notice_list = []
    if not os.path.exists(dir):
        os.makedirs(dir)
    for url in url_list:
        title = re.sub('[\/:*?"<>|]', '_', url[1])
        if ~is_cover:
            if os.path.exists(dir + '/' + title + '.txt'):
                continue
            
        print('[download_url]downloading url:  ' + url[0] + '  tittle: ' + url[1])
        try:
            html = requests.get(url[0], timeout = 10)
        except requests.exceptions.ConnectionError:
            print('[download_url]Error: url' + url[0] + 'connect failed!')
            continue
            
        new_notice_list.append(url)
        html.encoding = html.apparent_encoding
        result = html.text
        soup = BeautifulSoup(result, 'html.parser')
        tags = soup.find_all('p')
        date = re.findall(r'<div class="date_bar" >(.*?)</div>', result, re.S)
        text = 'url: ' + url[0] + '\r\n' + 'title: ' + url[1] + '\r\n' + 'date: ' + date[0] + '\r\n' + 'text: '
        for tag in tags:
            text = text + '\r\n' + tag.get_text()
        text_list.append(text)
        text_dir = dir + '/' + title + '.txt'
        fp = open(text_dir, 'wb')
        text = text.encode('utf-8')
        fp.write(text)
        fp.close()
    return new_notice_list