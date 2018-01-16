#(I guess class variables are like static stuff)
#class Dog:
    #kind = 'canine'         # class variable shared by all instances
    #def __init__(self, name):
        #self.name = name    # instance variable unique to each instance
#INSTANCE VARIBLES ARE DECLARED INSIDE THE "CONSTRUCTOR" WHICH IS __init__ method

#todo to do:
#This appears to be working perfectly...I just need to be sure that something went to both addresses below.
#Also I need to upload to the linux machine.
import sys

sys.path.append('''C:\james\projects\MyResources_linux''')
#sys.path.append('''/home/srlsph/logs/''')

import os
import datetime
import shutil
import csv
import xlsxwriter
import inspect


import sendEmail


#Progress: currently FileMover class tests fine by itself.
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#SPECIAL NOTE: to create a new action you would do this:

class TableManager:
    currentIndex = 0
    
    #Currently the only actions available are:
    #ytd, simpleExtractStorage, simpleExcelStorage
    filesTemplate = [
    ["","ytd","flexsite_uc_stats.txt","FlexSite Unit Code Statistics for YYYY.xls", "C:\\Management Reports\\2017 Management Reports"],
    ["","ytd","deptstat.txt","Dept UC Statistics Report for YYYY.xls", "C:\\Management Reports\\2017 Management Reports"],
    ["","ytd","h_pylori.txt","H Pylori Zip Report for YYYY.xls","C:\\Lab\\zFiles from the IT Department\\H pylori zip reports"],
    ["","ytd","jak2.txt","JAK2 Zip Report for YYYY.xls","C:\\Lab\\zFiles from the IT Department\\JAK2 zip reports"],
    ["","simpleExtractStorage","roche_hpv.txt","Roche YYYY HPV Statistics by zipcode.txt","C:\\Lab\\zFiles from the IT Department\\HPV by ZipCode Statistics Reports"],
    ["","ytd","thyretain.txt","YYYY Thyretain Report.xls","C:\\Lab\\zFiles from the IT Department\\Thyretain Zip Reports"],
    ["","simpleExcelStorage","anat_bill_tat.txt","YYYY anat bill stuff.xlsx","C:\Lab"]
    ]

    #actionTable = [
    #["ytd",],
    #[],
    #[],
    #]
    dateCol = 0
    actionCol = 1
    inputExtractCol = 2
    outputNameCol = 3
    destinationDirCol = 4

    def _setInputFolder(self):
        for i in range(0,len(self.filesTemplate)):
            self.filesTemplate[i][self.inputExtractCol] = os.path.join(FileMover.inputPath,self.filesTemplate[i][self.inputExtractCol])

    def iterateThroughTable(self):
        for i in range(0,len(self.filesTemplate)):
            self.currentIndex = i
            try:
                for fileName in os.listdir(FileMover.inputPath):
                    if self.filesTemplate[i][self.dateCol] in DateManager.yesterList or (self.filesTemplate[i][self.dateCol].lower() == "daily") or (self.filesTemplate[i][self.dateCol] == ""):
                        if os.path.join(FileMover.inputPath,fileName) == os.path.join(FileMover.inputPath,self.filesTemplate[i][self.inputExtractCol]):
                            self.sendToAction()
                            break
            except:
                e = ErrorManager()
                e.createError(str(inspect.stack()[0][3]), self.filesTemplate[self.currentIndex][inputExtractCol], "For loop access of file name in designated folder may have failed")
                e.sendError()
                e.logError()

    def sendToAction(self):
        manip = FileManipulator(os.path.join(FileMover.inputPath,self.filesTemplate[self.currentIndex][self.inputExtractCol]))
        fileMoveObj = FileMover()
        outputNameOfFile = self.filesTemplate[self.currentIndex][self.outputNameCol]
        outputDestination = self.filesTemplate[self.currentIndex][self.destinationDirCol]

        if self.filesTemplate[self.currentIndex][self.actionCol] == "ytd":
            manip.ytdProcess()
            fileMoveObj.writeListToXlsx(manip.currentCSVList,os.path.join(FileMover.outputPath,outputNameOfFile))
            fileMoveObj.copyFromOutputPath(outputNameOfFile, os.path.join(outputNameOfFile, outputDestination))
#            fileMoveObj.writeListToXlsx(manip.currentCSVList,os.path.join(self.filesTemplate[self.currentIndex][destinationDirCol],self.filesTemplate[self.currentIndex][self.outputNameCol]))
                        
        elif self.filesTemplate[self.currentIndex][self.actionCol] == "simpleExtractStorage":
            manip.extractStore()
            fileMoveObj.copyToOutputPath(self.filesTemplate[self.currentIndex][self.inputExtractCol],outputNameOfFile)
            fileMoveObj.copyFromOutputPath(outputNameOfFile, os.path.join(outputNameOfFile, outputDestination))
            
            
        elif self.filesTemplate[self.currentIndex][self.actionCol] == "simpleExcelStorage":
            manip.excelStore()
            fileMoveObj.writeListToXlsx(manip.currentCSVList,os.path.join(FileMover.outputPath,outputNameOfFile))
            fileMoveObj.copyFromOutputPath(outputNameOfFile, os.path.join(outputNameOfFile, outputDestination))
#            fileMoveObj.writeListToXlsx(manip.currentCSVList,os.path.join(self.filesTemplate[self.currentIndex][destinationDirCol],self.filesTemplate[self.currentIndex][self.outputNameCol]))
            
            
    def __init__(self):
#        print("bbb")
#        print(self.filesTemplate[0][self.inputExtractCol])#debug
#        self._setInputFolder()
        pass
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class ErrorManager:
    logDirectory = "outputDir"
    logFileName = "ErrorLogFile.txt"
    errorMessage = ""
    emailAddresses = ["jcarter@cpllabs.com","ck0fe@hotmail.com"]
    
    def __init__(self):
        pass

    def _lowLevelEmailFunction(self,messageToEmail, emailAddress):
        del sys.argv[1:]
        sys.argv.append('-r')
        sys.argv.append(emailAddress)
        sys.argv.append('-b')
        sys.argv.append(messageToEmail)
        sys.argv.append('--s')
        sys.argv.append("error message(s) for SOR script")
        sendEmail.main()        


    def createError(self,functionName, inputFile, details):
        self.errorMessage = ""
        self.errorMessage += "-------------------------------------------\n"
        self.errorMessage += "SOR script error\n"
        self.errorMessage += "date: " + str(DateManager.todayYear) + "/" +str(DateManager.todayMonth) + "/" + str(DateManager.todayDay) + ".  At " + str(DateManager.todayDate.hour) + ":" + str(DateManager.todayDate.minute)  + "\n"
        self.errorMessage += "File: " + str(inputFile) + " could not be processed.\n"
        self.errorMessage += "    In Function:" + functionName + ".\n"
#        self.errorMessage += "    In Class:   " + str(type(self.__class__.__name__) + ".\n"
#        self.errorMessage += "    In Class:   " + className + ".\n"
        self.errorMessage += "Error Details: " + str(details) + "\n"
        self.errorMessage += "-------------------------------------------\n\n"

    def sendError(self):
        print(self.errorMessage)
        for emailAddress in self.emailAddresses:
            self._lowLevelEmailFunction(self.errorMessage, emailAddress)


    def logError(self):
        print(ErrorManager.errorMessage)
        with open(os.path.join(self.logDirectory,self.logFileName),"a", newline = '') as fileWrite:
#        with open(self.logFileName,"a", newline = '') as fileWrite:            
            fileWrite.write(self.errorMessage)




#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class FileManipulator:
    currentCSVList = []

    def getListOfLists(self):
        return self.currentCSVList

    def ytdProcess(self):
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
        
        for i in range(1, DateManager.monthBeingProcessed +2):    #1 element for each month and also for YTD
            monthTotals.append("")
        
        originalRowLength = len(self.currentCSVList[0])
    
        #This 'if' block makes sure extract follows convention of having a header end with the months header columns always ending in DEC
        if self.currentCSVList[0][originalRowLength - 1][0:3].lower() != "dec":
            ErrorManager.sendErrorMessage()
            return -1
        if self.currentCSVList[0][originalRowLength - 2][0:3].lower() != "nov":
            ErrorManager.sendErrorMessage()
            return -1
        
        #rowLength = originalRowLength - (12 - yMonth)
    
        #Let's delete all columns fromoriginal extract that we dont' need...columns after the one for monthBeingProcessed and add the YTD column after that.
        for i in range(0,len(self.currentCSVList)):
            for j in range(originalRowLength - 12 + (DateManager.monthBeingProcessed - 1) + 1,originalRowLength):
                del self.currentCSVList[i][originalRowLength - 12 + (DateManager.monthBeingProcessed - 1) + 1:]
            if i == 0:              #Here add the extra column for YTD
                self.currentCSVList[i].append("YTD" + str(DateManager.yearBeingProcessed))
            else:
                self.currentCSVList[i].append("")
    
        #After reshaping the list of lists we reevaulte these variables
        finalRowLength = originalRowLength - 12 + DateManager.monthBeingProcessed + 1
        indexOfFirstMonth = originalRowLength - 12
    
        #Here in all cells where there should be number values...if the cell is blank then we input a zero.  This is to avoid problems in the program later on
        for i in range(1,len(self.currentCSVList)):
           for j in range(indexOfFirstMonth,finalRowLength - 1):
               if self.currentCSVList[i][j] == "":
                   self.currentCSVList[i][j] = "0"       #we make it a string because other values in csv they are string
    
    
        #rowLength += 1
        if len(self.currentCSVList) > 1:
            for i in range(1,len(self.currentCSVList)):
                ytdSum = 0
                for j in range(indexOfFirstMonth, finalRowLength - 1):
                    #the if-else section below needs to convert string ot a number or it won't add rather than concatenate a string.  converts to either int or float.  If we happen to hcomeacross a situation where int + float it dwon't mateter becuase it cast automatically to float.
                    if self.currentCSVList[i][j].find(".")!= -1:
                        tempNumber = float(self.currentCSVList[i][j])
                    else:
                        tempNumber = int(self.currentCSVList[i][j])
                    ytdSum += tempNumber
                self.currentCSVList[i][finalRowLength - 1] = str(ytdSum)
        else:
            pass
    
    
        #get sums for each individual month column and also YTD column:
        for i in range(0,len(monthTotals)):    #do each month in monthTotals
            tempTotal = 0
            for j in range(1,len(self.currentCSVList)):  #go down each row for the column corresponding to the month of the outer loop
                tempNumber = self.currentCSVList[j][indexOfFirstMonth + i]
    
                if self.currentCSVList[j][indexOfFirstMonth + i].find(".")!= -1:
                    tempNumber = float(tempNumber)
                else:
                    tempNumber = int(tempNumber)
                tempTotal += tempNumber
            monthTotals[i] = tempTotal
    
    
    
    
        #in the section below we add the last row which will have the totals:
        tempRow = []
        for j in range(0,finalRowLength):
            tempRow.append("")
        self.currentCSVList.append(tempRow[:])
        self.currentCSVList.append(tempRow[:])


        try:
            self.currentCSVList[len(self.currentCSVList)-1][indexOfFirstMonth - 1] = "TOTALS:"
        except:
            ErrorManager.generalExceptionHandler()
    


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
            self.currentCSVList[len(self.currentCSVList) - 1][i] = monthTotals[tempIndex]
            tempIndex += 1
                      
        
            
        
    def _initializeListOfLists(self):
        if len(self.currentCSVList) == 0:
            pass
        else:
            del self.currentCSVList[:]

    def _storeCSVAsList(self):
        del self.currentCSVList[:]
        with open(self.fileProcessedWithPathName,'r') as f:
            csv_f = csv.reader(f, delimiter = '\t')
            for row in csv_f:
                self.currentCSVList.append(row)
    
   

    def excelStore(self):
       pass
    

    def extractStore(self):
        pass
        
    def __init__(self, filePathAndName):
        self.fileProcessedWithPathName = filePathAndName
#        print(self.fileProcessedWithPathName)
        self._initializeListOfLists()
        self._storeCSVAsList()
#        print("in init")
#        print(self.currentCSVList[0])


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class FileMover:
    inputPath = "inputDir"
    outputPath = "outputDir"

    def getDefaultInputPath(self):
        return self.inputPath
    
    def getDefaultOutputPath(self):
        return self.outputPath
    
    def copyFromOutputPath(self, sourceFileName, destinationPathAndName):
        shutil.copy2(os.path.join(self.outputPath,sourceFileName), destinationPathAndName)

    def copyToOutputPath(self, sourceFileName, destinationFileName):
        shutil.copy2(os.path.join(self.inputPath,sourceFileName), os.path.join(self.outputPath,destinationFileName))
        
    def writeListToCSV(self, listToWrite, outputFile):
        with open(outputFile,"w", newline = '') as csv_file2:
            writer = csv.writer(csv_file2, delimiter='\t')
            for line in listToWrite:
                writer.writerow(line)
    
    def writeListToExcel(self, listToWrite, outputFile):
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1", cell_overwrite_ok = True)
        
        for i, l in enumerate(listToWrite):
            for j, col in enumerate(l):
                sheet1.write(i, j, col)
    #    book.save('exceldoc.xls')
        book.save(outputFile)
    
    def writeListToXlsx(self, listToWrite, outputFile):
        #This function uses the xlsxwriter package
        workbook = xlsxwriter.Workbook(outputFile)
        worksheet = workbook.add_worksheet()

        #format02 = workbook.add_format()
        #format02.set_num_format('#,##0')
        
        for i in range(0,len(listToWrite)):
            for j in range(0,len(listToWrite[i])):
                tempCell = listToWrite[i][j].replace(".","")
                tempCell = tempCell.replace(",","")
                if tempCell.isnumeric():
                    tempCell = float(tempCell)
#                    worksheet.write_number(i, j, tempCell, format02)
                    worksheet.write_number(i, j, tempCell)                    
                else:
                    worksheet.write_string(i, j, listToWrite[i][j])
        workbook.close()
                              
    
    def __init__(self):
        pass


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class DateManager:
    yesterList = []
    dayBeingProcessed = 0
    monthBeingProcessed = 0
    yearBeingProcessed = 0


    todayDate = datetime.datetime.now()
    yesterDate = todayDate - datetime.timedelta(1)
    todayYear = todayDate.year
    todayMonth = todayDate.month
    todayMonth = 9  #debug
    todayDay = todayDate.day
    
    yesterYear = yesterDate.year
    yesterMonth = yesterDate.month
    yesterMonth = 9 #debug
    yesterDay = yesterDate.day
    
    tempList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    todayDayOfTheWeek = tempList[datetime.datetime.today().weekday()]
    yesterDayOfTheWeek = tempList[yesterDate.weekday()]
    
    yesterList.append(yesterDayOfTheWeek)
    yesterList.append(yesterDayOfTheWeek.lower())
    yesterList.append(yesterDayOfTheWeek.upper())
    yesterList.append(yesterDayOfTheWeek.capitalize())
    yesterList.append(str(yesterDay))
    
    if yesterDay < 10:
        yesterList.append(str(yesterDay).zfill(2))
    
    if yesterMonth == 1:
        monthBeingProcessed = 12
    else:
        monthBeingProcessed = yesterMonth - 1
    if yesterMonth == 1:
        yearBeingProcessed = yesterYear - 1
    else:
        yearBeingProcessed = yesterYear


    def __init__(self):
        pass
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
        
#t = TableManager()
#t._setInputFolder()
#d = DateManager()


#print("-----------------")
#print("Testing FileMover class")
#f = FileMover()
#print(f.getDefaultInputPath())
#print(f.getDefaultOutputPath())
#f.copyToOutputPath("h_pylori.txt")
#f.copyToOutputPath("deptstat.txt")
#f.copyFromOutputPath("h_pylori.txt", os.path.join(t.filesTemplate[2][t.destinationDirCol],t.filesTemplate[2][t.outputNameCol]))
#f.copyFromOutputPath("deptstat.txt", os.path.join(t.filesTemplate[1][t.destinationDirCol],t.filesTemplate[1][t.outputNameCol]))


#--------------------------------
#TESTING ytdprocess()
#t2 = TableManager()
#ma2 = FileManipulator("C:\\james\projects\\cplSOR\\CodeFolder\\phase7\\inputDir\\flexsite_uc_stats.txt")
#f2 = FileMover()


#ma2.ytdProcess()
#f2.writeListToXlsx(ma2.currentCSVList,"test20180115.xlsx")


#--------------------------------
#testing def iterate
#t3 = TableManager()
#d3 = DateManager()
#t3.iterateThroughTable()

#--------------------------------
#testing error manager including the email part of it

def testFunction():
    e = ErrorManager()
    e.createError(str(inspect.stack()[0][3]), "filename2", "For loop access of file name in designated folder may have failed")
#    e.createError(inspect.stack()[0][3], "filename1", "For loop access of file name in designated folder may have failed")
    e.sendError()
    e.logError()

d4 = DateManager()
testFunction()
