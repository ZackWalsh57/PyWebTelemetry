#This program is going to simply find averages and estimate values when the machine is at an idle.

#Setup imports and explain why.
import os #Path searches
import csv #CSV and HML reading/writing
from collections import defaultdict #Parsing and saving collumn names
import time #Delays to stop the program from pulling stale/invalid values.

#Inform what this actually is.
print("================================================================================================\n")
print("\t\t\t\tPyWebTelem Data Analysis\n  This program will find the Min, Max, Average, and Idle values for the monitored components")
print("\t  Note: This will only computer idle values for the CPU and GPU. Not the RAM")
print("\n================================================================================================\n")

#Since this code is going to change when added into the final program, it will not ask for a path.
#It will use the default path (Since that's what works for me)
DEFAULT_PATH = 'C:/Program Files (x86)/MSI Afterburner/HardwareMonitoring.hml' #ProgFiles default
PATH_LOCATION = DEFAULT_PATH

#Since we have to treat this as a standalone program, we have to parse and read the hml file and 
#do the whole CSV conversion BS again.
CSV_OUTPUT = 'CSV_OUTPUT.csv' #This file is temporary!!!!
print("Determining Measurement blocks....\n") 

with open(PATH_LOCATION, "rb") as INPUT: #Open the log file and call it the input
    INPUT.next() #Since the logs are always going to have two lines of bs, skip.
    INPUT.next()
    with open(CSV_OUTPUT, "w") as OUTPUT: #Write OUTPUT file.
        CSV_WRITTER = csv.writer(OUTPUT) #CSV Writer begins
        for row in csv.reader(INPUT): #For each row in the input file...
            CSV_WRITTER.writerow(row[2:]) #Write said row BEGINING AFTER THE 2ND
            
with open(CSV_OUTPUT) as UNSORTED: #Read the temporary file
    SORTER = csv.DictReader(UNSORTED, delimiter =',')
    DATA_FIELDS_TRAILING = SORTER.fieldnames #Fieldnames is just collumn names
    DATA_FIELDS = [] #Empty list for the measurement blocks
    for MEAS_BLOCK in DATA_FIELDS_TRAILING: #Print them out in a neat order.
        STRIPPED = MEAS_BLOCK.strip() #Remove Whitespace
        DATA_FIELDS.append(STRIPPED) #Append the new strings to the list
    print("Measurement Blocks")
    for ITEM in DATA_FIELDS:
        print("- " + ITEM)
    print("\n================================================================================================\n")

#Now begins the new code which we havent used before.
#It grabs the log files and saves the measurements one by one, adding up the total and dividing it by the number of itterations.

#Lists for the average temperatures, uses, and so on. This list MUST be the same size as the DATA_FIELDS list so they can be
#Zipped and easily modified. ITTERATIONS marks how many requests we make. Bad requests will be ignored!!!! 
#The mins and maxes are also stored in a list of the same length. One list for min and one for max.
#It works like this:
#   CPU Temp = 30  | GPU Temp = 25 | and so on...
#   Once read, itterations is bumped up by one.
#   Each index which contains the work usage is then divided by the itterations value and stored in averages.
#   For min and max, we just compare the new value to the last lowest value.
MIN_USAGE_TEMP = [0] * len(DATA_FIELDS)     #Minimum recorded number for the usage and temps
MAX_USAGE_TEMP = [0] * len(DATA_FIELDS)     #Maximum recorded number for the usage and temps

#ITTERATIONS = 0                            #Counts how many loops we run.  Used for average calculations.

#Show the empty lists to prove they are empty and exist.
print("Creating lists for logging....")
print("Zeroing the lists....\n")
print "Minimums | ", MIN_USAGE_TEMP
print "Maximums | ", MAX_USAGE_TEMP 
MIN_USAGE_TEMP = [1000000] * len(DATA_FIELDS)
print("\n================================================================================================\n")

#Now we go into the actual logging process.
#Make the average logger a while loop since that's how it would run in the actual program
#Make sure that we use try/except to prevent errors.
print("Logging now. Minimums and Maximums shown below.\n")

while True:
    time.sleep(1)
    INDEX = 0
    try:
        #This code is copied right from the live logger. 
        with open(PATH_LOCATION) as RAW_MEAS_BLOCKS: #Opens the log file
            VALUE_READER = csv.reader(RAW_MEAS_BLOCKS) #Read the log file
            for SKIP_COUNT in range(10): #Skip those 10 worthless lines
                next(VALUE_READER) #Line 11 is what we want.
            RAW_ROW = next(VALUE_READER) #This is line 11 
            VALUES_RAW = RAW_ROW[2:] #Copy all the values after coll 2
            VALUES_CLEAN = [] #Empty list for stripped monitored values
            for RAW_VALUES in VALUES_RAW: 
                STRIPPED = RAW_VALUES.strip() #Strip whitespace
                VALUES_CLEAN.append(STRIPPED) #Save them
                STRIPPED_INT = STRIPPED
    except:
        print("\nPULLED TOO FAST\n")        
    
    if INDEX < len(VALUES_CLEAN):
        for VALUE in VALUES_CLEAN:
            if float(VALUE) > float(MAX_USAGE_TEMP[INDEX]):
                MAX_USAGE_TEMP[INDEX] = VALUE
            INDEX += 1
        INDEX = 0
        
        for VALUE in VALUES_CLEAN:
            if float(VALUE) < float(MIN_USAGE_TEMP[INDEX]):
                MIN_USAGE_TEMP[INDEX] = VALUE
            INDEX += 1
        INDEX = 0
    
    print "\nVal | ", VALUES_CLEAN
    print "Min | ", MIN_USAGE_TEMP
    print "Max | ", MAX_USAGE_TEMP

    try:
        os.remove(PATH_LOCATION)
    except:
        print("DELETION ERROR")    

