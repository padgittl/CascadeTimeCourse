import sys, re, os
from Bio import SeqIO
from Bio.Seq import Seq

###############
# SUBROUTINES #
###############

def readAndFilterFasta(fastaFile,refStatus):
    geneDict = {}
    fullPath = fastaFile.strip() 
    fileName = os.path.basename(fullPath)
    filePrefix,fileExt = os.path.splitext(fileName) 
    # TCONS_00000193 gene=000000F.g1
    # loop through all transcripts and append to dict of lists keyed by geneID
    for record in SeqIO.parse(fastaFile,"fasta"):
        #print record.id,record.name,record.description
        getGeneID = re.search('gene=(.+)',record.description)
        geneID = getGeneID.group(1)
        #print geneID
        if geneID not in geneDict:
            geneDict[geneID] = []
        geneDict[geneID].append((record.id,len(record.seq)))
    
    # sort for longest transcript length per gene
    for geneID in geneDict:
        geneDict[geneID].sort(key=lambda x:x[1], reverse=True)

    # keep longest transcript only 
    longestTranscripts = {}
    for geneID in geneDict:
        recordID,recordLen = geneDict[geneID][0]
        #print geneID,recordID,recordLen
        if recordID not in longestTranscripts:
            longestTranscripts[recordID] = geneID

    '''            
    for recordID in longestTranscripts:
	print recordID
    '''
    # loop through fasta again to keep only the longest transcript per gene
    filteredRecordDict = {}
    filteredRecordList = []
    for record in SeqIO.parse(fastaFile,"fasta"):
        if record.id in longestTranscripts:
            #print record.id
            if record.id not in filteredRecordDict:
                filteredRecordDict[record.id] = 1
                filteredRecordList.append(record)
    SeqIO.write(filteredRecordList,"longestTranscriptPerGene_" + refStatus + ".fasta", "fasta")
    return(longestTranscripts)


def writeFilteredGFF(gffFile,longestTranscripts):
    OUT = open("longestTranscriptPerGene_" + refStatus + ".gff",'w')
    transcriptCountDict = {}
    for line in open(gffFile,'r'):
        if not line.startswith('#'):
            contigID,source,feature,start,end,score,strand,frame,attribute = line.strip().split("\t")
            # 000000F Cufflinks       transcript      157113  157342  .       -       .       ID=TCONS_00000073;geneID=XLOC_000052
            # 000000F Cufflinks       exon    157113  157342  .       -       .       Parent=TCONS_00000073
            if feature == 'transcript':
                getTranscriptID = re.search('(TCONS_\d+);gene',attribute)
                transcriptID = getTranscriptID.group(1)
                #print transcriptID
	        if transcriptID in longestTranscripts:
		    #print transcriptID
                    transcriptCountDict[transcriptID] = 1
                    OUT.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (contigID,source,feature,start,end,score,strand,frame,attribute))
            elif feature == 'exon':
                getTranscriptID = re.search('Parent=(TCONS_\d+)',attribute)
                transcriptID = getTranscriptID.group(1)
                if transcriptID in longestTranscripts:
                    OUT.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (contigID,source,feature,start,end,score,strand,frame,attribute))
            else:
                print "other feature"
                sys.exit()
    print len(transcriptCountDict)



########
# MAIN #
########

usage = "Usage: " + sys.argv[0] + " <fasta file> <gff file> <with or without ref, e.g. 'noRef' or 'withRef'>\n"
if len(sys.argv) != 4:
    print usage
    sys.exit()

fastaFile = sys.argv[1]
gffFile = sys.argv[2]
refStatus = sys.argv[3]

longestTranscripts = readAndFilterFasta(fastaFile,refStatus)
writeFilteredGFF(gffFile,longestTranscripts)
