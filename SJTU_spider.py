#!/usr/bin/env python
# coding: utf-8

from notice import notice
from spider import SEIEE_xsb_spider

dir = './data/SEIEE_xsb'
notice_list = SEIEE_xsb_spider.SEIEE_xsb_spider_get_new(dir)
notice.send_notice(notice_list, 'xsb')