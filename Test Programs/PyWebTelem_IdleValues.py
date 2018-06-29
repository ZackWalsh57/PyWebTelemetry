#This file is going to demonstrate how we can save idle temps for the desired components.
#It will log the values to establish a base idle usage for components by doing this:
#   Check the monitored components and only pick out the CPU and GPU values.
#   See current value of each components use and temp.
#   If the current value is below a cutoff, save that temp and use it as an idle temp for that component.
#   Rinse and repeat. 
#       For the CPU, we'll say idle use is between 0 and 15%.
#       For the GPU, we'll say idle use is between 0 and 30% for each one.

#Setup imports and explain why.
import os #Path searches
import csv #CSV and HML reading/writing
from collections import defaultdict #Parsing and saving collumn names
import time #Delays to stop the program from pulling stale/invalid values.

#Get some data....
print("================================================================================================\n")
print("\t\t\t\tPyWebTelem Data Analysis\n  \t\t\tThis program will find the average temps at idle.\n")
print("================================================================================================\n")


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

#Now we figure out where our idle use values are.
#We read each index of the DATA_FIELDS list and find which ones are named CPU and GPU.
print("\t Index Locations")
INDEX = 0
USAGE_INDICIES = []
USAGE_TYPE = []
TEMP_INDICIES = []
TEMP_TYPE = []

for VALUES in DATA_FIELDS:
    STRING = str(VALUES)
    if (STRING.__contains__("CPU") and STRING.__contains__("usage")):
        print "At index: ", INDEX, "    |   ", STRING
        USAGE_INDICIES.append(INDEX)
        USAGE_TYPE.append(STRING)
    if (STRING.__contains__("GPU") and STRING.__contains__("usage")):
        print "At index: ", INDEX, "    |   ", STRING   
        USAGE_INDICIES.append(INDEX)
        USAGE_TYPE.append(STRING)
    if (STRING.__contains__("CPU") and STRING.__contains__("temperature")):
        TEMP_INDICIES.append(INDEX)
        TEMP_TYPE.append(STRING)
    if (STRING.__contains__("GPU") and STRING.__contains__("temperature")):
        TEMP_INDICIES.append(INDEX)
        TEMP_TYPE.append(STRING)
    INDEX += 1

USAGE_PAIRS = zip(USAGE_INDICIES, USAGE_TYPE)
TEMP_PAIRS = zip(TEMP_INDICIES, TEMP_TYPE)

print("\nPaired Indicies and Value Table.")
print USAGE_PAIRS,
print "\n", TEMP_PAIRS
print("\nThe first value is the index.  The second one is the value.")

print("\n================================================================================================\n")

#These paired lists are nice because they serve as a lookup table now.  
#We can call USAGE_PAIRS[0][1] to find out what usage is stored at index 0.
#From there, we can search the index in the pair and use it to store values.

#LOGIC
#   Find which item in the usage pairs we need by reading the values from the usage indicies.
#       Each index and value pair can be read as a string. So if we have USAGE_PAIRS[0] equal to
#           0, CPU usage, we can read index 0 to get CPU Usage.
#       Knowing we have the cpu usage, we can check if it's lower than the threshold.
#       If it is lower, then we look at the TEMP_PAIRS and locate the index for the temp of the CPU.
#           Look at each item in the temp pairs.  Find that TEMP_PAIRS[0] is 1, CPU temperature.
#           Then, we store CPU temperature as an idle temp in a list.
#
# This is repeated for the GPU idle temps.
# NOTE: If that made no sense look at the readme of this folder.

# More work on this will be done in the future. I'm considering making a globalized dictionary 
#that has a the index and name of each monitored component/value for easier lookups. 