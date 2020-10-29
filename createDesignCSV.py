import os,re,sys
import numpy as np

'''
sample,condition
CascadeA_DroughtHeat,DroughtHeat
CascadeA_DroughtControl,DroughtControl
CascadeB_DroughtControl,DroughtControl
CascadeC_DroughtControl,DroughtControl
CascadeB_DroughtHeat,DroughtHeat
CascadeC_DroughtHeat,DroughtHeat
'''

def createDesignCSV(geneCountMatrixFile):
    OUT = open('design.csv','w')
    OUT.write("sample,condition\n")
    with open(geneCountMatrixFile,'r') as F:
        for line in F:
		# gene_id,E1,E10,E2,E4,E5,E6,E7,E8,E9,L10,L11,L12,L13,L5,L6,L7,L8,L9,M1,M2,M3,M4,M5,M6,M7,M8,M9
		if line.startswith('gene_id'):
			line = line.strip().split(',')
			# print line
			for sampleID in line:
				if not sampleID == 'gene_id':
					if 'E' in sampleID:
				                developmentStageID = 'Early'	
				                OUT.write("%s,%s\n" % (sampleID,developmentStageID))
			                elif 'M' in sampleID:
				                developmentStageID = 'Mid'
				                OUT.write("%s,%s\n" % (sampleID,developmentStageID))
			                else:	
				                developmentStageID = 'Late'
				                OUT.write("%s,%s\n" % (sampleID,developmentStageID))	


########
# MAIN #
########

usage = "Usage: " + sys.argv[0] + " <gene count matrix file> \n"
if len(sys.argv) != 2:
    print usage
    sys.exit()

geneCountMatrixFile = sys.argv[1]

createDesignCSV(geneCountMatrixFile)
