# -*- coding: utf-8 -*-
import json
import re
import numpy
import glob
from matplotlib import pyplot

for F in glob.glob("followers*json")[0:]:
    pyplot
    with open(F, 'r') as jsonFile:
        who = re.search("followers-(\S*).json", F).group(1)
        dat = json.loads(jsonFile.read())
        N = len(dat)
        #print F, N 
        eggs = []
        nils = []
        years = {}
        for i, c in dat.iteritems():
            if (c["egg"]):
                eggs.append(i)
                if (c["profile length"] == 0) :
                    nils.append(c["n statuses"])
            year = int(str(c["created_at"])[:4])
            if year in years:
                years[year] += 1
            else:
                years[year] = 1
        print who, len(eggs), 100*len(eggs)/N, nils.count(0), nils.count(0)*100/N,\
            numpy.median(years.keys())

        yx = []
        yy = []

        for y in sorted( years.keys() ):
            yx.append(y)
            yy.append(years[y])

        pyplot.bar(range(len(yy)), yy)
        pyplot.xticks(range(len(yx)), yx, rotation=15)
        pyplot.xlabel(u'années de création des followers')
        pyplot.title("@%s n=%d"%(who, N))
        pyplot.savefig("%s.png"%who)
        pyplot.close()



