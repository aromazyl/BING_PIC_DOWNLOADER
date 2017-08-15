#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 zhangyule <zyl2336709@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import urllib2
import json
import sys
import os
from multiprocessing.pool import Pool as ThreadPool


def get_json(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        print('cannot read %s' % url)
        return None

def get_url(url):
    try:
        pase = json.loads(get_json(url))
        return 'https://cn.bing.com/' + pase['images'][0]['url']
    except:
        print('cannot load', get_json(url), ',url:', url)
        return None

def bingDayUrl(day):
    return 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1&mkt=en-US' % day

def get_pic_name(url):
    if url == None:
        return ''
    name = json.loads(get_json(url))['images'][0]['copyright'].split(None, 1)[0] + '.jpg'
    return name

def downloadfile((url,name)):
    if url == None or name == None:
        return None
    if os.path.exists("./" + name):
        print 'Downloaded', name
        return None
    else:
        print 'NewPicture', name
    text = urllib2.urlopen(url).read()
    f = open(name, 'w')
    f.write(text)
    f.close()

#print get_url('http://www.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1&mkt=en-US' % 1)
#print '\n'.join(get_bing_pic(-1, 1))
# print get_pic_name(get_url('http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'))

def lazyWrap(func, x):
    return lambda: func(x)

def forEach(func, cases):
    for case in cases:
        func(case)

def download_pic_range(i, j):
    pool = ThreadPool()
    links = pool.map(bingDayUrl, range(i, j+1))
    pic_urls = pool.map(get_url, links)
    pic_name = pool.map(get_pic_name, links)
    pool.map(downloadfile, zip(pic_urls, pic_name))

if __name__ == '__main__':
    download_pic_range(int(sys.argv[1]), int(sys.argv[2]))
