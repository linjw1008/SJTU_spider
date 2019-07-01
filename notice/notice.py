#!/usr/bin/env python
# coding: utf-8

import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def send_email(text, from_name, to_name, from_addr, password, to_addr, smtp_server, tittle):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'<%s> <%s>' %(from_name, from_addr))
    msg['To'] = _format_addr(u'<%s> <%s>' %(to_name, to_addr))
    msg['Subject'] = Header(u'<%s>' %tittle, 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_notice(notice_list, web_name):
    if len(notice_list) == 0:
        return False
    from_name = 'SJTU_spider'
    to_name = 'SJTU_spider_user'
    from_addr = 'linjw1008@163.com'
    to_addr = 'linjw1008@163.com'
    smtp_server = 'smtp.163.com'
    password = input('Password: ')
    text = 'Get the following new notices from %s：' % web_name
    i = 1
    for notice in notice_list:
        text = text + '\r\n' + '[' + str(i) + ']' + 'NOTICE: ' + notice[1] + '   URL: ' + notice[0]
        i += 1
    send_email(text, from_name, to_name, from_addr, password, to_addr, smtp_server, 'New notice form <%s>' %web_name)
    
    return True

