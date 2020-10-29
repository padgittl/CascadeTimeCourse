import sys, re, os


###############
# SUBROUTINES #
###############


def readFileList(fileList):
    totalNumberReads = 0
    totalUniquelyMappedReadPercentage = 0
    totalNumberReps = 0
    totalMappedPercentageAllSamples = 0
    
    with open(fileList,'r') as F:
        for line in F:
            totalNumberReps += 1
            fileName = line.strip()
            numberInputReads,uniquelyMappedReadPercentage,totalMappedPercentage = readOutFile(fileName)
            totalNumberReads += numberInputReads
	    # print totalNumberReads,totalNumberReps
            totalUniquelyMappedReadPercentage += uniquelyMappedReadPercentage
	    totalMappedPercentageAllSamples += totalMappedPercentage
            #print numberInputReads,totalNumberReads,totalNumberReps
    avgNumberReads = float(totalNumberReads) / totalNumberReps
    # print totalNumberReads,totalNumberReps,avgNumberReads
    avgNumberReadsPerMillion = avgNumberReads / 1000000
    avgUniquelyMappedReadPercentage = float(totalUniquelyMappedReadPercentage) / totalNumberReps
    avgMappedPercentageAllSamples = float(totalMappedPercentageAllSamples) / totalNumberReps
    # print("Average Number of Reads:\t%s\t" % (avgNumberReadsPerMillion))
    # print("Average Uniquely Mapped Read Percent:\t%s\t" % (avgUniquelyMappedReadPercentage))
    print("Average Mapped Percentage - Unique and Multi:\t%s\t" % (avgMappedPercentageAllSamples))

# https://github.com/alexdobin/STAR/issues/282
# mapped to too many loci is categorized as unmapped

def readOutFile(outFile):
    fullPath = outFile.strip() 
    fileName = os.path.basename(fullPath)
    filePrefix,fileExt = os.path.splitext(fileName) 
    # lane1-s025-indexRPI28-CAAAAG-L11_S25_L001Log.final.out
    # lane1-s001-indexRPI21-GTTTCG-E1_S1_L001Log.final
    getRunID = re.search('(.+)\Log\.final',filePrefix)
    runID = getRunID.group(1)
    # print runID
    with open(outFile,'r') as O:
        for line in O:
            if 'Number of input reads' in line:
                info,numberInputReads = line.strip().split('|')
                numberInputReads = numberInputReads.strip()
                numberInputReads = int(numberInputReads)
            elif 'Average mapped length' in line:
                info,averageMappedLength = line.strip().split('|')
                averageMappedLength = averageMappedLength.strip()
                averageMappedLength = float(averageMappedLength)
            elif 'Uniquely mapped reads number' in line:
                info,uniquelyMappedReadNumber = line.strip().split('|')
                uniquelyMappedReadNumber = uniquelyMappedReadNumber.strip()
                uniquelyMappedReadNumber = int(uniquelyMappedReadNumber)
            elif 'Number of reads mapped to multiple loci' in line:
                info,readsMappedMultipleLociNumber = line.strip().split('|')
                readsMappedMultipleLociNumber = readsMappedMultipleLociNumber.strip()
                readsMappedMultipleLociNumber = int(readsMappedMultipleLociNumber)
            elif 'Number of reads mapped to too many loci' in line:
                info,readsMappedTooManyLociNumber = line.strip().split('|')
                readsMappedTooManyLociNumber = readsMappedTooManyLociNumber.strip()
                readsMappedTooManyLociNumber = int(readsMappedTooManyLociNumber)
                
                uniquelyMappedReadPercentage = round(100 * (float(uniquelyMappedReadNumber) / numberInputReads), 3)
                readsMappedMultipleLociPercentage = round(100 * (float(readsMappedMultipleLociNumber) / numberInputReads), 3)
                totalMappedPercentage = round(100 * (float(uniquelyMappedReadNumber + readsMappedMultipleLociNumber) / numberInputReads), 3)

                print("%s\t%s\t%s\t%s\t%s\t%s\t" % (runID,numberInputReads,averageMappedLength,uniquelyMappedReadPercentage,readsMappedMultipleLociPercentage,totalMappedPercentage))
    return(numberInputReads,uniquelyMappedReadPercentage,totalMappedPercentage)

########
# MAIN #
########

usage = "Usage: " + sys.argv[0] + " <star final out file list>\n"
if len(sys.argv) != 2:
    print usage
    sys.exit()

fileList = sys.argv[1]

print "run_ID\ttotal_number_input_reads\taverage_mapped_length\tmapped_uniquely_percentage\tmapped_multiple_loci_percentage\ttotal_mapped_percentage\t"
readFileList(fileList)

