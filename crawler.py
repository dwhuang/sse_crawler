#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import socket
import time
from lxml import etree
import json
import re
from sections import sections

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
                time.sleep(5)
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
        #print "read complete: " + fname
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
    # create cache dir
    try:
        os.mkdir("cache")
    except OSError:
        pass
    # fetch stock ids and shortnames
    indexurl = "http://www.sse.com.cn/disclosure/listedinfo/regular/"
    stocklist = getIndex(indexurl, "index.html")
    # for each stock/company
    alldata = []
    for (stockid, shortname) in stocklist:
        companydata = {"id": stockid, "shortname": shortname, "data": []}
        for (sectname, secturl, rowtitles) in sections:
            url = baseurl + secturl + "?stock_id=" + stockid \
                    + "&report_year=2015&report_period_id=5000"
            sectfname = stockid + "-" + sectname
            rawdata = fetch(url, sectfname)
            try:
                rawdata = json.loads(rawdata)
            except ValueError as e:
                print "***** section has no data"
                print e
                print stockid, sectname, url
                companydata['data'].append([]) # note empty list
                continue
            # sanity check: check for inconsistent number of rows
            if len(rowtitles) != len(rawdata['rows']):
                print "***** num row titles ", len(rowtitles), \
                        " != num rows ", len(rawdata['rows'])
            # get column titles: (fieldname, year)
            coltitles = []
            for col in rawdata['columns'][0]:
                coltitles.append((col['field'], col['title']))
            # get data in each row
            sectdata = []
            for row in rawdata['rows']:
                rowdata = []
                for col in coltitles:
                    if col[0] in row:
                        field = row[col[0]]
                    else:
                        field = ""
                    if isinstance(field, basestring):
                        # strip <div>
                        field = re.sub(r"<\/?div.*?>", "", field)
                        # replace <br> with ;
                        field = re.sub(r"<\/?br.*?>", ";", field)
                    rowdata.append((col[1], field))
                sectdata.append(rowdata)
            companydata['data'].append(sectdata)
        alldata.append(companydata)
    # save
    jsondata = json.dumps(alldata, ensure_ascii=False).encode('utf-8')
    with open('data.json', 'wb') as f:
        f.write(jsondata)

if __name__ == '__main__':
    main()
