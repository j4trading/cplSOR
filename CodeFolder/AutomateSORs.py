import csv
import os
import datetime
"""

"""
#This program assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months header columns always ending in DEC

#To DO TODO:
#Make it send an email if it fails...I have an unwritten function sendErrorMessage() for that purpose
#Currenty this program assumes that we are working off of its own directory
#   a function to bring other extracts into its directory might need to be added

#DIfferent types of extract formats

todayDate = datetime.datetime.now()
todayYear = todayDate.year
todayMonth = todayDate.month

currentCSVList = []   #this is a list of lists which holds the values of a csv

def initializeListOfLists(csvList):
    if len(csvList) == 0:
        pass
    else:
        del csvList[:]

def storeCSVAsList(fileName,outputList):
    del outputList[:]
    with open(fileName,'r') as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            outputList.append(row)

def writeListToCSV(listToWrite, outputFile):
    with open(outputFile,"w", newline = '') as csv_file2:
        writer = csv.writer(csv_file2, delimiter=',')
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
    rowLength = 0
    monthTotals = []
    
    if todayMonth == 1:
        monthBeingProcessed = 12
    else:
        monthBeingProcessed = todayMonth - 1

    if todayMonth == 1:
        yearBeingProcessed = todayYear - 1
    else:
        yearBeingProcessed = todayYear
    print(monthBeingProcessed)

    for i in range(1, monthBeingProcessed +2):    #1 element for each month and also for YTD
        monthTotals.append("")
    
    originalRowLength = len(currentCSVList[0])

    #This 'if' block makes sure extract follows convention of having a header end with the months header columns always ending in DEC
    if currentCSVList[0][rowLength-1][0:1].lower != "dec":
        sendErrorMessage()
        return
    if currentCSVList[0][rowLength-2][0:1].lower != "nov":
        sendErrorMessage()
        return
    
    rowLength = originalRowLength - (12 - todayMonth)

    #Let's delete all columns fromoriginal extract that we dont' need...columns after the one for monthBeingProcessed
    for i in range(0,len(currentCSVList)):
        for j in range(originalRowLength - 12 + (monthBeingProcessed - 1) + 1,originalRowLength):
            del currentCSVList[i][originalRowLength - 12 + (monthBeingProcessed - 1) + 1:]


    currentCSVList[0].append("YTD" + str(yearBeingProcessed))
    rowLength += 1
    if len(currentCSVList) > 1:
        for i in range(1,len(currentCSVList)):
            currentCSVList[i].append("")
            ytdSum = 0
            for j in range(originalRowLength - 12,rowLength - 1):
                #the if-else section below needs to convert string ot a number or it won't add rather than concatenate a string.  converts to either int or float.  If we happen to hcomeacross a situation where int + float it dwon't mateter becuase it cast automatically to float.
                if currentCSVList[i][j].find(".")!= -1:
                    tempNumber = float(currentCSVList[i][j])
                else:
                    tempNumber = int(currentCSVList[i][j])
                ytdSum += tempNumber
            currentCSV[i][rowLength-1] = ytdSum
    else:
        pass


    #get sums for each individual month column and also YTD column:
    for i in range(0,len(monthsTotals)):    #do each month in monthsTotals
        tempTotal = 0
        for j in range(1,len(currentCSVList)):  #go down each row for the column corresponding to the month of the outer loop
            tempNumber = currentCSVList[j][originalRowLength-12+i]
            if currentCSVList[i][j].find(".")!= -1:
                tempNumber = float(tempNumber)
            else:
                tempNumber = int(tempNumber)
            tempTotal += tempNumber
        monthsTotals[i] = tempTotal




    #in the section below we add the last row which will have the totals:
    tempRow = []
    for j in range(0,rowLength):
        tempRow.append("")
    currentCSVList.append(tempRow)
    currentCSVList.append(tempRow)
    try:
        currentCSVList[len(currentCSVList)-1][originalRowLength - 12 - 1] = "TOTALS:"
    except:
        generalExceptionHandler()

    tempIndex = 0
    for i in range(originalRowLength-12, rowLength):
        currentCSVList[len(currentCSVList) - 1][i] = monthTotals[tempIndex]
        tempIndex += 1

    #print(len(currentCSVList))
    print("in function")

def generalExceptionHandler():
    pass #sendEmailthing

                  

def sendErrorMessage():
    pass


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#THSI IS THE MAIN SECTION

initializeListOfLists(currentCSVList)
storeCSVAsList('flexsite_uc_stats.txt',currentCSVList)
manipulateTypicalMonthly()
writeListToCSV(currentCSVList,'flex_test.csv')
#print(currentCSVList)
print(len(currentCSVList))
#---------------------------------------------------------------------
#---------------------------------------------------------------------
