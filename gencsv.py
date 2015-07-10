#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import re
import sys
from sections import sections

def getYearVal(datafield, year=""):
    if year == "":
        # get most recent year
        mostrecentyear = 0
        mostrecentind = -1
        for ind, entry in enumerate(datafield):
            if entry[1] == '' or entry[1] == 0 or entry[1] == '-':
                continue
            if mostrecentyear < entry[0]:
                mostrecentyear = entry[0]
                mostrecentind = ind
        if mostrecentind < 0:
            return ''
        return datafield[mostrecentind][1]
    else:
        for entry in datafield:
            if entry[0] == year:
                return entry[1]
        return ''

def main(argv):
    """
    Generate a csv file for each section. Each row contains a company and each
    column contains a data field.  The value for each field is taken from
    the most recent year available.
    """
    if len(argv) > 0:
        year = argv[0]
    else:
        year = ""

    with codecs.open("results/data.json", "rb", "utf-8") as fp:
        data = json.load(fp)

    for secind, (secname, securl, secfields) in enumerate(sections):
        with codecs.open(year + secname + ".csv", "wb", "utf-8-sig") as fp:
            # title row
            fp.write(u"股票代码,简称," + ",".join(secfields) + "\n")
            for company in data:
                fp.write(company['id'] + "," + company['shortname'] + ",")
                vals = []
                for field in company['data'][secind]:
                    v = getYearVal(field, year)
                    if isinstance(v, basestring):
                        v = re.sub(r'"', '""', v)
                        v = '"' + v + '"'
                    else:
                        v = unicode(v)
                    vals.append(v)
                fp.write(",".join(vals) + "\n")

if __name__ == '__main__':
    main(sys.argv[1:])

# Usage: first argument year; optional. If not specified, will try to find the
# most recent value.
