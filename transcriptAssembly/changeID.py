import os,re,sys
import numpy as np


def changeID(gtfList):
    OUT = open('sampleIDs.txt','w')
    with open(gtfList,'r') as F:
        for line in F:
            fileName = line.strip()
            #fileName = os.path.basename(fullPath)
            # lane1-s001-indexRPI21-GTTTCG-E1_S1_L001_coordSorted.gtf
            # sample18         lane1-s018-indexRPI26-ATGAGC-M9_S18_L001_coordSorted.gtf
            # sample19         lane1-s019-indexRPI15-ATGTCA-L5_S19_L001_coordSorted.gtf
	    # getRunInfo = re.search('(.+)_S\d+_L001_coordSorted.gtf',fileName)
	    getRunInfo = re.search('(.+)_S\d+_L001.+gtf',fileName)
            runInfo = getRunInfo.group(1)
            runInfo = runInfo.split('-')
            developmentStage = runInfo[4]
            #print developmentStage
    	    OUT.write("%s\t%s\n" % (developmentStage,fileName))


########
# MAIN #
########

usage = "Usage: " + sys.argv[0] + " <gtf list> \n"
if len(sys.argv) != 2:
    print usage
    sys.exit()

gtfList = sys.argv[1]

changeID(gtfList)
