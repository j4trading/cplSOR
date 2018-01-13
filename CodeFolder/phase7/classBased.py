#(I guess class variables are like static stuff)
#class Dog:
    #kind = 'canine'         # class variable shared by all instances
    #def __init__(self, name):
        #self.name = name    # instance variable unique to each instance
#INSTANCE VARIBLES ARE DECLARED INSIDE THE "CONSTRUCTOR" WHICH IS __init__ method

import os
import datetime

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class TableManager:
    currentIndex = 0
    
    filesTemplate = [
    ["","ytd","flexsite_uc_stats.txt","FlexSite Unit Code Statistics for YYYY.xls", "C:\\Management Reports\\2017 Management Reports"],
    ["","ytd","deptstat.txt","Dept UC Statistics Report for YYYY.xls", "C:\\Management Reports\\2017 Management Reports"],
    ["","ytd","h_pylori.txt","H Pylori Zip Report for YYYY.xls","C:\\Lab\\zFiles from the IT Department\\H pylori zip reports"],
    ["","ytd","jak2.txt","JAK2 Zip Report for YYYY.xls","C:\\Lab\\zFiles from the IT Department\\JAK2 zip reports"],
    ["","ytd","roche_hpv.txt","Roche YYYY HPV Statistics by zipcode.xls","C:\\Lab\\zFiles from the IT Department\\HPV by ZipCode Statistics Reports"],
    ["","ytd","thyretain.txt","YYYY Thyretain Report.xls","C:\\Lab\\zFiles from the IT Department\\Thyretain Zip Reports"],
    ]
    dateCol = 0
    actionCol = 1
    inputExtractCol = 2
    outputNameCol = 3
    destinationDirCol = 4

    def _setInputFolder(self):
        print(FileMover.inputPath)
        for i in range(0,len(self.filesTemplate)):
            self.filesTemplate[i][self.inputExtractCol] = os.path.join(FileMover.inputPath,self.filesTemplate[i][self.inputExtractCol])

    def iterateThroughTable():
        for i in range(0,len(self.filesTemplate)):
            currentIndex = i
            for fileName in os.listdir(FileMover.inputPath):
                if filesTemplate[i][self.dateCol] in DateManager.yList or (self.filesTemplate[i][dateCol].lower() == "daily") or (self.filesTemplate[i][self.dateCol] == ""):
                    if os.path.join(FileMover.inputPath,fileName) == self.filesTemplate[i][self.inputExtractCol]:
    #                    completeName = os.path.join(inputDir, fileName)
                        processAndSaveFile(self.filesTemplate[i][self.inputExtractCol], i)
                        break
                

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class ErrorManager:
    def __init__(self):
        pass

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class FileManipulator:
    currentCSVList = []

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
        #This function uses the xlsxwriter package
        workbook = xlsxwriter.Workbook(outputFile)
        worksheet = workbook.add_worksheet()

        format02 = workbook.add_format()
        format02.set_num_format('#,##0')
        
        for i in range(0,len(listToWrite)):
            for j in range(0,len(listToWrite[i])):
                tempCell = listToWrite[i][j].replace(".","")
                tempCell = tempCell.replace(",","")
                if tempCell.isnumeric():
                    tempCell = float(tempCell)
                    worksheet.write_number(i, j, tempCell, format02)
                else:
                    worksheet.write_string(i, j, listToWrite[i][j])
        workbook.close()
    

    def excelStorage():
       pass
    

    def extractStorage():
        pass
        
    def __init__(self):
        self.initializeListOfLists(self.currentCSVList)
#        self.storeCSVAsList(inputPathAndFile, self.currentCSVList)
        

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class FileMover:
    inputPath = "inputDir"
    outputPath = "outputDir"

    def getDefaultInputPath(fileName):
        pass
    def getDefaultOutputPath(fileName):
        pass
    
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

    def __init__(self):
        todayDate = datetime.datetime.now()
        yesterDate = todayDate - datetime.timedelta(1)
        todayYear = todayDate.year
        todayMonth = todayDate.month
        #todayMonth = 9
        todayDay = todayDate.day
    
        yesterYear = yesterDate.year
        yesterMonth = yesterDate.month
        yesterDay = yesterDate.day
    
        tempList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        todayDayOfTheWeek = tempList[datetime.datetime.today().weekday()]
        yesterDayOfTheWeek = tempList[yesterDate.weekday()]
    
        self.yesterList.append(yesterDayOfTheWeek)
        self.yesterList.append(yesterDayOfTheWeek.lower())
        self.yesterList.append(yesterDayOfTheWeek.upper())
        self.yesterList.append(yesterDayOfTheWeek.capitalize())
        self.yesterList.append(str(yesterDay))
    
        if yesterDay < 10:
            self.yesterList.append(str(yesterDay).zfill(2))
    
        if yesterMonth == 1:
            self.monthBeingProcessed = 12
        else:
            self.monthBeingProcessed = yesterMonth - 1
        if yesterMonth == 1:
            self.yearBeingProcessed = yesterYear - 1
        else:
            self.yearBeingProcessed = yesterYear


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
        
t = TableManager()
t._setInputFolder()
d = DateManager()
print(d.yesterList)
print(d.dayBeingProcessed)
print(d.monthBeingProcessed)
print(d.yearBeingProcessed)

