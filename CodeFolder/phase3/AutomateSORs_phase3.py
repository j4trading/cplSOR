#from github
import csv
import os
import datetime
"""
"""
#This program assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months header columns always ending in DEC

#12/30/2017:
#completely correctly does the main kidnof file that you find in 1st of the month...but i wish there was a way to make this work for creating .xls files

#To DO TODO:
#Make it send an email if it fails...I have an unwritten function sendErrorMessage() for that purpose
#Currenty this program assumes that we are working off of its own directory
#   a function to bring other extracts into its directory might need to be added

#DIfferent types of extract formats
#if there was a way to create an excel file out of it.

todayDate = datetime.datetime.now()
todayYear = todayDate.year
todayMonth = todayDate.month

inputPath = "inputDir"
outputPath = "outputDir"

if todayMonth == 1:
    monthBeingProcessed = 12
else:
    monthBeingProcessed = todayMonth - 1
if todayMonth == 1:
    yearBeingProcessed = todayYear - 1
else:
    yearBeingProcessed = todayYear



currentCSVList = []   #this is a list of lists which holds the values of a csv

def initializeListOfLists(csvList):
    if len(csvList) == 0:
        pass
    else:
        del csvList[:]

def storeCSVAsList(fileName,outputList):
    del outputList[:]
    with open(fileName,'r') as f:
        csv_f = csv.reader(f, delimiter = '\t')
        for row in csv_f:
            outputList.append(row)

def writeListToCSV(listToWrite, outputFile):
    with open(outputFile,"w", newline = '') as csv_file2:
        writer = csv.writer(csv_file2, delimiter='\t')
        for line in listToWrite:
            writer.writerow(line)   

def manipulateTypicalMonthly():
#This function assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months header columns always ending in DEC
#FUnction assumes that the month we are processing it for is the month previous to the date on which it is being processed.

#"""
#THIS IS THE ORIGINAL STATE OF THE EXTRACT
#header:          c1 c2 c2 jan feb mar apr may jun jul aug sep oct nov dec
# count:           1  2  3  4   5   6   7   8   9   10   1   12 13  14 15
#element Index:    0  1  2  3   4   5   6   7   8   9
#
#
#END RESULT of program for CSV FILE:
#header:        c1 c2 c2 jan feb mar apr may YTD2017
#count:         1  2  3  4   5   6   7   8   9   
#element index: 0  1  2  3   4   5   6   7   8   
#                     t: SM1 SM2 SM3 SM4 SM5 SM6
#"""
    originalRowLength = 0
#    rowLength = 0
    monthTotals = []
    
    for i in range(1, monthBeingProcessed +2):    #1 element for each month and also for YTD
        monthTotals.append("")
    
    originalRowLength = len(currentCSVList[0])

    #This 'if' block makes sure extract follows convention of having a header end with the months header columns always ending in DEC
    if currentCSVList[0][originalRowLength - 1][0:3].lower() != "dec":
        sendErrorMessage()
        return
    if currentCSVList[0][originalRowLength - 2][0:3].lower() != "nov":
        sendErrorMessage()
        return
    
    #rowLength = originalRowLength - (12 - todayMonth)

    #Let's delete all columns fromoriginal extract that we dont' need...columns after the one for monthBeingProcessed and add the YTD column after that.
    for i in range(0,len(currentCSVList)):
        for j in range(originalRowLength - 12 + (monthBeingProcessed - 1) + 1,originalRowLength):
            del currentCSVList[i][originalRowLength - 12 + (monthBeingProcessed - 1) + 1:]
        if i == 0:              #Here add the extra column for YTD
            currentCSVList[i].append("YTD" + str(yearBeingProcessed))
        else:
            currentCSVList[i].append("")

    #After reshaping the list of lists we reevaulte these variables
    finalRowLength = originalRowLength - 12 + monthBeingProcessed + 1
    indexOfFirstMonth = originalRowLength - 12

    #Here in all cells where there should be number values...if the cell is blank then we input a zero.  This is to avoid problems in the program later on
    for i in range(1,len(currentCSVList)):
       for j in range(indexOfFirstMonth,finalRowLength - 1):
           if currentCSVList[i][j] == "":
               currentCSVList[i][j] = "0"       #we make it a string because other values in csv they are string


    #rowLength += 1
    if len(currentCSVList) > 1:
        for i in range(1,len(currentCSVList)):
            ytdSum = 0
            for j in range(indexOfFirstMonth, finalRowLength - 1):
                #the if-else section below needs to convert string ot a number or it won't add rather than concatenate a string.  converts to either int or float.  If we happen to hcomeacross a situation where int + float it dwon't mateter becuase it cast automatically to float.
                if currentCSVList[i][j].find(".")!= -1:
                    tempNumber = float(currentCSVList[i][j])
                else:
                    tempNumber = int(currentCSVList[i][j])
                ytdSum += tempNumber
            currentCSVList[i][finalRowLength - 1] = str(ytdSum)
    else:
        pass


    #get sums for each individual month column and also YTD column:
    for i in range(0,len(monthTotals)):    #do each month in monthTotals
        tempTotal = 0
        for j in range(1,len(currentCSVList)):  #go down each row for the column corresponding to the month of the outer loop
            tempNumber = currentCSVList[j][indexOfFirstMonth + i]

            if currentCSVList[j][indexOfFirstMonth + i].find(".")!= -1:
                tempNumber = float(tempNumber)
            else:
                tempNumber = int(tempNumber)
            tempTotal += tempNumber
        monthTotals[i] = tempTotal




    #in the section below we add the last row which will have the totals:
    tempRow = []
    for j in range(0,finalRowLength):
        tempRow.append("")
    currentCSVList.append(tempRow[:])
    currentCSVList.append(tempRow[:])
    try:
        currentCSVList[len(currentCSVList)-1][indexOfFirstMonth - 1] = "TOTALS:"
    except:
        generalExceptionHandler()

    for i in range(0,len(monthTotals)):
        monthTotals[i] = str(monthTotals[i])
        if monthTotals[i].find(".") == -1:
            monthTotals[i] = int(monthTotals[i])
            monthTotals[i] = "{:,}".format(monthTotals[i])
        else:
            monthTotals[i] = float(monthTotals[i])
            monthTotals[i] = "{:,}".format(monthTotals[i])


    tempIndex = 0
    for i in range(indexOfFirstMonth, finalRowLength):
        currentCSVList[len(currentCSVList) - 1][i] = monthTotals[tempIndex]
        tempIndex += 1


def easyProcess():
    pass  #nothing to do

def generalExceptionHandler():
    pass #sendEmailthing


def sendErrorMessage():
    pass


def iterateThroughFiles():
    for i in range(0,len(filesTemplate)):
        filesTemplate[i][1] = os.path.join(inputPath,filesTemplate[i][1])
        filesTemplate[i][2] = os.path.join(outputPath,filesTemplate[i][2])

    print(inputPath)
    for fileName in os.listdir(inputPath):
        for i in range(0,len(filesTemplate)):
            if os.path.join(inputPath,fileName) == filesTemplate[i][1]:
#                completeName = os.path.join(inputDir, fileName)
                processAndSaveFile(filesTemplate[i][1], i)
                break

def processAndSaveFile(inputPathAndFile, passedIndex):
    initializeListOfLists(currentCSVList)
    storeCSVAsList(inputPathAndFile, currentCSVList)
    outputFile = filesTemplate[passedIndex][2]
    monthString = str(monthBeingProcessed)
    if monthBeingProcessed < 10:
        monthString = (str(monthBeingProcessed)).zfill(2)
    else:
        monthString = str(monthBeingProcessed)
    yearString = (str(yearBeingProcessed))

    if outputFile.find("YYYY") != -1:
        print(outputFile)
        print(yearString)
        outputFile = outputFile.replace("YYYY", yearString,1)
        print("xx")
        print(outputFile)
    elif outputFile.find("YY") != -1:
        outputFile = outputFile.replace("YY", yearString[2:4],1)

    if outputFile.find("MM") != -1:
        outputFile = outputFile.replace("MM",monthString,1)
        
    if filesTemplate[passedIndex][0] == "ytd":
        manipulateTypicalMonthly()        
    elif filesTemplate[passedIndex][0] == "easyProcess":
        easyProcess()

    writeListToCSV(currentCSVList, outputFile)

    

#These show what type of file it is...inptut file to look for, output file to do, and destination location
filesTemplate = [
    #type,  inputfile,  outputFile,  destination
["ytd", "flexsite_uc_stats.txt",  "FlexSite Unit Code Statistics for YYYY.xls", "S:\Management Reports\2017 Management Reports"],
["ytd", "deptstat.txt", "Dept UC Statistics Report for YYYY.xls", "S:\Management Reports\2017 Management Reports"]
]

#---------------------------------------------------------------------
#---------------------------------------------------------------------
#THSI IS THE MAIN SECTION before phase 2
#initializeListOfLists(currentCSVList)
#storeCSVAsList('flexsite_uc_stats.txt',currentCSVList)
#manipulateTypicalMonthly()
#writeListToCSV(currentCSVList,'flex_test.xls')

#---------------------------------------------------------------------
#This is the current designed workflow of the program:
#First call iterateThroughFiles
#That function will iterate and look up the files that are in the directory and look them up in the filesTemplate

#ProcessAndSaveFile then is call within the iterations:
#It initializes the list that holds the spreadsheet
#It decides what the outputFile should be named
#And based on the cell 'type' cell element it decides which data processing function should be called
# Finally it calls the function that writes from list ot CSV file

#iterateThroughFiles("\dir")
#-------------------------------------------------------
#This is the main section at phase3
iterateThroughFiles()
#-------------------------------------------------------
