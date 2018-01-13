import csv
import os
import datetime
import xlrd
import xlwt
from shutil import copyfile
from shutil import copy2
import xlsxwriter

def writeCsvToXlsx(listToWrite, outputFile):
    workbook = xlsxwriter.Workbook(outputFile)
    worksheet = workbook.add_worksheet()
#    worksheet.write_row('A4', listToWrite[0])
    #worksheet.write_row('A5', listToWrite[1])
    #worksheet.write_row('A6', listToWrite[2])
    #worksheet.write_row('A7', listToWrite[3])
    for i in range(0,len(listToWrite)):
        for j in range(0,len(listToWrite[i])):
#            worksheet.write_string  (row, col,     item              )
#     worksheet.write_datetime(row, col + 1, date, date_format )
#     worksheet.write_number  (row, col + 2, cost, money_format)
            if listToWrite[i][j].replace(".","").isnumeric():
                listToWrite[i][j] = float(listToWrite[i][j])
                worksheet.write_number(i, j, listToWrite[i][j])
            else:
                worksheet.write_string(i, j, listToWrite[i][j])
    workbook.close()



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



currentCSVList = []   #this is a list of lists which holds the values of a csv


filesTemplate = [
[r"",r"ytd", r"flexsite_uc_stats.txt",  r"FlexSite Unit Code Statistics for YYYY.xls", r"C:\Management Reports\2017 Management Reports"],
[r"",r"ytd", r"deptstat.txt", r"Dept UC Statistics Report for YYYY.xls", r"C:\Management Reports\2017 Management Reports"],
[r"",r"ytd",r"h_pylori.txt",r"H Pylori Zip Report for YYYY.xls",r"C:\Lab\zFiles from the IT Department\H pylori zip reports"],
[r"",r"ytd",r"jak2.txt",r"JAK2 Zip Report for YYYY.xls",r"C:\Lab\zFiles from the IT Department\JAK2 zip reports"],
[r"",r"ytd",r"roche_hpv.txt",r"Roche YYYY HPV Statistics by zipcode.xls",r"C:\Lab\zFiles from the IT Department\HPV by ZipCode Statistics Reports"],
[r"",r"ytd",r"thyretain.txt",r"YYYY Thyretain Report.xls",r"C:\Lab\zFiles from the IT Department\Thyretain Zip Reports"],
]

dateCol = 0
actionCol = 1
inputExtractCol = 2
outputNameCol = 3
destinationDirCol = 4

initializeListOfLists(currentCSVList)
storeCSVAsList("test1.txt",currentCSVList)
writeCsvToXlsx(currentCSVList, "delete/testOutput.xlsx")
