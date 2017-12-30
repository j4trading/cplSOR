import csv
import os
"""

"""
#This program assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months folowed by the YTD column header

#To DO TODO:
#Make it send an email if it fails...I have an unwritten function sendErrorMessage() for that purpose
#Currenty this program assumes that we are working off of its own directory
#   a function to bring other extracts into its directory might need to be added

todayDate = datetime.datetime.now()
todayYear = todayDate.year
todayMonth = todayDate.month

def storeCSVAsList(fileName,outputList):
    del outputList[:]
    with open(fileName,'r') as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            outputList.append(row)
    

def manipulateTypicalMonthly(extract, outputCSV):
#This function assumes that the csv file has a header row
#It also assumes that all of their input extracts' headers end with the months folowed by the YTD column header
    rowLength = 0
    csvList = []
    
    storeCSVAsList(extract, csvList)
    rowLength = len(csvList[0])
#This if block makes sure extract follows convention of having a header that ends with the months and finally with the YTD column
    if currentCSVList[0][rowLength-1][0:2

def sendErrorMessage():
    pass
