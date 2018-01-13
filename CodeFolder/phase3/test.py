import csv
import os
#directory = "C:\james\projects\cplSOR\CodeFolder\phase3\dir"

outputList = []

directory = "dir"

name_of_file = "flexsite_uc_stats.txt"
save_path = "dir"
completeName = os.path.join(save_path, name_of_file)         


#for fileName in os.listdir(directory):
#	print(fileName)    


del outputList[:]
with open(completeName,'r') as f:
    csv_f = csv.reader(f, delimiter = '\t')
    for row in csv_f:
        outputList.append(row)

print (outputList[0])
