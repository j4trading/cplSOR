import csv
import os
import datetime
import xlrd
import xlwt
from shutil import copyfile
from shutil import copy2
import xlsxwriter
"""
"""
#This program assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months header columns always ending in DEC

#12/30/2017:
#completely correctly does the main kidnof file that you find in 1st of the month...but i wish there was a way to make this work for creating .xls files

#1/4/18
#AFTER phase 4 it iteratees through well
#after phase 5 it iterates well and this includes checking on the date to see if it is tiem to run

#To DO TODO:
#Make it send an email if it fails...I have an unwritten function sendErrorMessage() for that purpose
#Currenty this program assumes that we are working off of its own directory
#   a function to bring other extracts into its directory might need to be added
# 1/4/16 at phase 4  fIRST I need to get this thing working
#     After that: I will come back and make this object oriented
#     The reason for that is that there are too many dependencies among the code.
#     FOr example process.... function calls manipulate.... function which exits  out of itself if the input extract is not in the expected format.
#     but the calling function process.... still outputs to excel file regardless.....so I need the inelegant passing of return value to process.... so that it can decide whether or not to create the excel file.
# The files that you stick into outputDir...after it gets done it needs to be stuck into a Processed directory

#Progress 1/8/18
#I'm at OUtputPhase()
#    It still needs work
#    I want to keep outputPath whether or not we do a TestMode...because we would still need ot keep a record of all the files that we created
#    But whether or not we use the destinationPath stuff will depend on testMode
#    After I finally get this to run I want to see if I can organize this much better

#End goal:
# This needs to be able to run off of the linux server
#iT SHOUDL look in a predetermined path determined by a variable
#ti will probably be scheduled daily by chron in linux
#each day it will look in that folder and compare to the table
#"the table" will have all of the SOR stuff that you have been used to processing
#     for each of those it will have:
#     date to process or the term weekly or daily, extract name, output file name, action to be done identifier (which associates with a function, destination folder, and comments section
#I think for weekly and daily files that need no processing on it of any sort I will just ask Scott if he has a script to put them in.
# At the end of that program: if something is in the table and it should've have been processed that day but it didn't then it will send a message to the error manager class.  This will be at the en dof the program...or at least at the end of the iterating
#     the error manager class will send out an error if an erro rhas not yet been sent.
#DIfferent types of extract formats
#if there was a way to create an excel file out of it.
#Finally it needs to tuck it away somewhere

#This program assumes that
testMode = 1  #0 means no test mode...otherwise it is in test mode
todayDate = datetime.datetime.now()
yDate = todayDate - datetime.timedelta(1)
todayYear = todayDate.year
todayMonth = todayDate.month
#todayMonth = 9
todayDay = todayDate.day
yYear = yDate.year
yMonth = yDate.month
yDay = yDate.day

tempList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
todayDayOfTheWeek = tempList[datetime.datetime.today().weekday()]
yDayOfTheWeek = tempList[yDate.weekday()]

yList = []
yList.append(yDayOfTheWeek)
yList.append(yDayOfTheWeek.lower())
yList.append(yDayOfTheWeek.upper())
yList.append(yDayOfTheWeek.capitalize())
yList.append(str(yDay))
if yDay < 10:
    yList.append(str(yDay).zfill(2))

inputPath = "inputDir"
outputPath = "outputDir"

if yMonth == 1:
    monthBeingProcessed = 12
else:
    monthBeingProcessed = yMonth - 1
if yMonth == 1:
    yearBeingProcessed = yYear - 1
else:
    yearBeingProcessed = yYear



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

def writeListToExcel(listToWrite, outputFile):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1", cell_overwrite_ok = True)
    
    for i, l in enumerate(listToWrite):
        for j, col in enumerate(l):
            sheet1.write(i, j, col)
#    book.save('exceldoc.xls')
    book.save(outputFile)

def writeListToXlsx(listToWrite, outputFile):
    workbook = xlsxwriter.Workbook(outputFile)
    worksheet = workbook.add_worksheet()
    for i in range(0,len(listToWrite)):
        for j in range(0,len(listToWrite[i])):

            if listToWrite[i][j].replace(".","").isnumeric():
                listToWrite[i][j] = float(listToWrite[i][j])
                worksheet.write_number(i, j, listToWrite[i][j])
            else:
                worksheet.write_string(i, j, listToWrite[i][j])
    workbook.close()

def excelStorage():
   pass


def extractStorage():
    pass

def manipulateTypicalMonthly():
#This function assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months header columns always ending in DEC
#FUnction assumes that the month we are processing it for is the month previous to the date on which it is being processed.
# right now returns a -1 if function fails.that way calling function knows not to right to excel file
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
        return -1
    if currentCSVList[0][originalRowLength - 2][0:3].lower() != "nov":
        sendErrorMessage()
        return -1
    
    #rowLength = originalRowLength - (12 - yMonth)

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

#This function is in charge of managing filesTemplate and dealing with the the input path folder
#Possible candidate classes to replace this function are for filesTemplateManager and directoryManager
def iterateThroughFiles():
    print("start")
    dayList = []
    del dayList[:]
    dayList.append
    
    for i in range(0,len(filesTemplate)):
        filesTemplate[i][inputExtractCol] = os.path.join(inputPath,filesTemplate[i][inputExtractCol])
#        if testMode != 0:
#            filesTemplate[i][destinationDirCol] = outputPath
        

    for fileName in os.listdir(inputPath):
        for i in range(0,len(filesTemplate)):
            if filesTemplate[i][dateCol] in yList or (filesTemplate[i][dateCol].lower() == "daily") or (filesTemplate[i][dateCol] == ""):
                if os.path.join(inputPath,fileName) == filesTemplate[i][inputExtractCol]:
#                    completeName = os.path.join(inputDir, fileName)
                    processAndSaveFile(filesTemplate[i][inputExtractCol], i)
                    break
                
def processFileName(outputFile):
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
    return outputFile
    

def processAndSaveFile(inputPathAndFile, passedIndex):
    functionReturn = 0
    initializeListOfLists(currentCSVList)
    storeCSVAsList(inputPathAndFile, currentCSVList)
    outputFile = filesTemplate[passedIndex][outputNameCol]

    print("before processfilename: ",outputFile)
    outputFile = processFileName(outputFile)
    print("after processfilename: ",outputFile)

    for s in range(0,len(filesTemplate)):
        filesTemplate[s][outputNameCol] = outputFile

    if filesTemplate[passedIndex][actionCol] == "ytd":
        functionReturn = manipulateTypicalMonthly()
    elif filesTemplate[passedIndex][actionCol] == "easyProcess":
        functionReturn = easyProcessPrep()
    elif filesTemplate[passedIndex][actionCol] == "extractStorage":
        functionReturn = extractStoragePrep(filesTemplate[passedIndex][inputExtractCol],currentCSVList)
    elif filesTemplate[passedIndex][actionCol] == "excelStorage":
        functionReturn = excelStoragePrep(filesTemplate[passedIndex][outputNameCol], currentCSVList)
        

#    if functionReturn != -1:
#        writeListToCSV(currentCSVList, outputFile)
##       writeListToExcel(currentCSVList, outputFile)

    if functionReturn != -1:
        outputPhase(passedIndex)
        copyToDestinationFolders(passedIndex)
    

def extractStoragePrep(inputFile, outputList):
    initializeListOfLists(outputList)
    with open(inputFile, 'r') as f:
        for line in f:
            outputList.append(line)
    return 1

def excelStoragePrep(outputFile, inputList):
    storeCSVAsList(fileName,outputList)
    return 1    

def listToExtract(outputFile, inputList):
    with open(inputFile, 'w') as f:
        for line in inputList:
            f.writeline(line)
    return 1
    

def outputPhase(passedIndex):
    currentCSVList
    outputFileAndPath = os.path.join(outputPath,filesTemplate[passedIndex][outputNameCol])
    print("in outputPhase: ", outputFileAndPath)
    print(currentCSVList[0])
    if filesTemplate[passedIndex][actionCol] == "ytd":
        writeListToXlsx(currentCSVList, outputFileAndPath)
#    elif filesTemplate[passedIndex][actionCol] == "easyProcess":
#        functionReturn = easyProcess()
    elif filesTemplate[passedIndex][actionCol] == "extractStorage":
        listToExtract(outputFileAndPath,currentCSVList)        
    elif filesTemplate[passedIndex][actionCol] == "excelStorage":
        writeListToXlsx(currentCSVList, outputFileAndPath)

def copyToDestinationFolders(passedIndex):
    outputFileAndPath = os.path.join(outputPath,filesTemplate[passedIndex][outputNameCol])
    print(outputFileAndPath)
    print(os.path.join(filesTemplate[passedIndex][destinationDirCol], filesTemplate[passedIndex][outputNameCol]))
    print("at error: ",filesTemplate[passedIndex][destinationDirCol], " ",filesTemplate[passedIndex][outputNameCol], " ",filesTemplate[passedIndex][inputExtractCol])
    copy2(outputFileAndPath, os.path.join(filesTemplate[passedIndex][destinationDirCol], filesTemplate[passedIndex][outputNameCol]))
   #abc123 

#These show what type of file it is...inptut file to look for, output file to do, and destination location
    #date to process, actionID,  inputfile,  outputFile,  destination
#The date column specifies on which days that extract will be processed.  It is a list so that it can run an ony of those days
#acceptable values are any digit for a day of the month, any string in ....monday, tuesday, , .....etc..case insensitive since I plan on making the code this way
    #but in the table I'll stick to using this format: Monday, Tuesday, Wednesday....etc...
    #also acceptable "daily"....
    #if it's blank it defaults to daily
#filesTemplate = [
#["","ytd", "flexsite_uc_stats.txt",  "FlexSite Unit Code Statistics for YYYY.xls", "S:\Management Reports\2017 Management Reports"],
#["","ytd", "deptstat.txt", "Dept UC Statistics Report for YYYY.xls", "S:\Management Reports\2017 Management Reports"],
#["","ytd","h_pylori.txt","H Pylori Zip Report for YYYY.xls","S:\Lab\zFiles from the IT Department\H pylori zip reports"],
#["","ytd","jak2.txt","JAK2 Zip Report for YYYY.xls","S:\Lab\zFiles from the IT Department\JAK2 zip reports"],
#["","ytd","roche_hpv.txt","Roche YYYY HPV Statistics by zipcode.xls","S:\Lab\zFiles from the IT Department\HPV by ZipCode Statistics Reports"],
#["","ytd","thyretain.txt","YYYY Thyretain Report.xls","S:\Lab\zFiles from the IT Department\Thyretain Zip Reports"],
#]

filesTemplate = [
[r"",r"ytd", r"flexsite_uc_stats.txt",  r"FlexSite Unit Code Statistics for YYYY.xls", "C:\\Management Reports\\2017 Management Reports"],
[r"",r"ytd", r"deptstat.txt", r"Dept UC Statistics Report for YYYY.xls", "C:\\Management Reports\\2017 Management Reports"],
[r"",r"ytd",r"h_pylori.txt",r"H Pylori Zip Report for YYYY.xls","C:\\Lab\\zFiles from the IT Department\\H pylori zip reports"],
[r"",r"ytd",r"jak2.txt",r"JAK2 Zip Report for YYYY.xls","C:\\Lab\\zFiles from the IT Department\\JAK2 zip reports"],
[r"",r"ytd",r"roche_hpv.txt",r"Roche YYYY HPV Statistics by zipcode.xls","C:\\Lab\\zFiles from the IT Department\\HPV by ZipCode Statistics Reports"],
[r"",r"ytd",r"thyretain.txt",r"YYYY Thyretain Report.xls","C:\\Lab\\zFiles from the IT Department\\Thyretain Zip Reports"],
]


dateCol = 0
actionCol = 1
inputExtractCol = 2
outputNameCol = 3
destinationDirCol = 4


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
for r in range(0,len(filesTemplate)):
    print(r"check")
#    print(r"\201")
    print(filesTemplate[r][destinationDirCol])
iterateThroughFiles()
#-------------------------------------------------------
