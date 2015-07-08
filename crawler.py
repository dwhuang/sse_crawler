#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from lxml import etree

def fetch(url, fname, encoding='utf-8'):
    fname = "cache/" + fname
    if not os.path.exists(fname):
        # Query URL if cache file does not already exist
        for i in range(10):
            # try 10 times
            try:
                r = requests.get(url, timeout=30)
                break
            except (requests.exceptions.Timeout, socket.timeout):
                print "fetch timed out, try again..."
                if i == 9:
                    raise RuntimeError("connection timed out, tried 10 times",
                            url, fname)
        r.encoding = encoding
        content = r.text
        if encoding is not None:
            content = content.encode(encoding)
        with open(fname, 'wb') as f:
            f.write(content)
        print "fetch complete: " + fname
    else:
        # Read the cache file
        with open(fname, 'rb') as f:
            content = f.read()
        print "read complete: " + fname
    return content

def getIndex(url, fname, encoding='utf-8'):
    content = fetch(url, fname)
    # parse html
    parser = etree.HTMLParser()
    root = etree.fromstring(content, parser)
    table = root.find(".//table[@id='listedcompany']")
    if table is None:
        raise RuntimeError("cannot find main table in the index file")
    alist = table.findall(".//a")
    # get the list
    ret = []
    for a in alist:
        # a tag text format: stockid(shortname), need to rid the parens
        (stockid, shortname) = a.text.strip()[:-1].split("(")
        ret.append((stockid, shortname))
    return ret

def main():
    baseurl = "http://listxbrl.sse.com.cn"
    taburls = {u"基本信息": "/companyInfo/showmap.do",
            u"股本結構": "/capital/showmap.do",
            u"前十大股東": "/companyInfo/showTopTenMap.do",
            u"資產負債表": "/companyInfo/showBalance.do",
            u"利潤表": "/profit/showmap.do",
            u"現金流量表": "/cash/showmap.do",}
    # create cache dir
    try:
        os.mkdir("cache")
    except OSError:
        pass
    # fetch stock ids and shortnames
    indexurl = "http://www.sse.com.cn/disclosure/listedinfo/regular/"
    stocklist = getIndex(indexurl, "index.html")
    # fetch tabs for each stocks
    for (stockid, shortname) in stocklist:
        for (tabname, taburl) in taburls.items():
            url = baseurl + taburl + "?stock_id=" + stockid \
                    + "&report_year=2015&report_period_id=5000"
            tabfname = stockid + "-" + tabname
            fetch(url, tabfname)

if __name__ == '__main__':
    main()
