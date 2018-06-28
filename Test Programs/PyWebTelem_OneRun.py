#This script is going to read live data from MSI Afterburner's file log feature and
#parse it locally for now.

#NOTE: THIS IS A ONE AND DONE SCRIPT FOR TESTING ONLY!!!!
#NOTE: THE FINAL PRODUCT WILL BE RUN WITH CONCURRENT THREADS FOR LIVE LOGS

#When the logging is working 100% we can then move into streaming that data to a web
#page/host and display it on graphs, along with calculating useful values like 
#   Avg Temps, Avg Use, Idle Temps, FPS, and so on.  


#Imports and reasons why
#os - Used for checking file existance.
#csv - Used for reading the .hml file
#defaultdict - Used to get coll names
#time - Used to log time and pause running.

import os
import csv
from collections import defaultdict
import time

#Lock onto the file we are going to be reading from. Allow the user to specify file location
#The default location is "C:\Users\ProgramFiles(x86)\MSI Afterburner\HardwareMonitoring.hml"
#But since nothing ever works the way it should, we're going to let the user decide where it should look.
print("======================================================================================\n")
print("\t\t\t      PyWebTelemetry V1.0\n\t      This program NEEDS MSI Afterburner installed to work!")
print("\t       RivaTuner MIGHT also work, but I have not tested it")
print("\nStart Afterburner, right click the graphs on the bottom and click \"Log to file\".")
print("Once started, enter the log file location INCLUDING the file name.")
print("Default Path: \"C:/Program Files (x86)/MSI Afterburner/HardwareMonitoring.hml\n")
print("    THIS PROGRAM *MUST* BE RUN AS AN ADMIN IF YOUR LOG IS OUTSIDE YOUR USER FOLDER")
print("======================================================================================\n")
#Here we ask the user to specify the file location as a string. As long as we dont have a file that exists,
#The prompt will loop.

#VALID_PATH is a basic boolean variable which flips from 0 to 1 when a valid path is seen.
#And since nobody wants to type this shit out, just make the default path an option.
VALID_PATH = 0
DEFAULT_PATH = 'C:/Program Files (x86)/MSI Afterburner/HardwareMonitoring.hml'

#While the bool VALID_PATH is not 1 (Or the path is not given/does not exist) run this loop
while VALID_PATH != 1:
    print("Enter the log file location using \'/\'. (Leave blank for default)")
    PATH_LOCATION = raw_input("Path: ") #Capture the path supplied now.
    
    #If the user doesnt give a path, use default.
    if PATH_LOCATION == "": PATH_LOCATION = DEFAULT_PATH

    print "Checking: ", PATH_LOCATION #Tell user the program is checking their path.
    if os.path.exists(PATH_LOCATION): #Now for a real check of the path.
        print("File exists! Preparing to parse now\n")
        try:
            os.remove(PATH_LOCATION)
            VALID_PATH = 1 #Flip the bool to exit the loop.
            time.sleep(1)
        except WindowsError:
            print("LOG FILE IN RESTRICTED PATH. Run again as admin for this to work.")
    else: #If something is an absolute SNAFU:
        print("Log file not found. Try again\n")
        VALID_PATH = 0 #No file found or invalid path, leave the bool restart the while loop.

#Now we move into the actual process of converting this jumbled mess into a numpy array or text file we can read from.
#I think the best way is to make a 2D Array for every component.  Since the files are split by commas, there has to be
#a way to seperate each collumn.
print("======================================================================================\n")
print("Opening file and start parse now....")

#Convert to a legit CSV file to find what the user wants recorded
CSV_OUTPUT = 'CSV_OUTPUT.csv'
print("\nFinding user desired measurments. This is a one time process!!")

#For the final product, this is going to become a looping program.
#It's going to read the .hml file, write those values into some sort of structure,
#then from there, delete the .hml, and pass the values recorded into a parser.

#Just do a one go for now...

#Cleanup the first two colls.
print("Cleaning up extra lines...")
with open(PATH_LOCATION, "rb") as INPUT: #Open the log file and call it the input
    INPUT.next() #Since the logs are always going to have two lines of bs, skip.
    INPUT.next()
    with open(CSV_OUTPUT, "w") as OUTPUT: #Write OUTPUT file.
        CSV_WRITTER = csv.writer(OUTPUT) #CSV Writer begins
        for row in csv.reader(INPUT): #For each row in the input file...
            CSV_WRITTER.writerow(row[2:]) #Write said row BEGINING AFTER THE 2ND
            

print("Determining wanted measurements...")
with open(CSV_OUTPUT) as UNSORTED:
    SORTER = csv.DictReader(UNSORTED, delimiter =',')
    DATA_FIELDS_TRAILING = SORTER.fieldnames
    DATA_FIELDS = []
    print("\n\t\tMeasurement Blocks")
    for MEAS_BLOCK in DATA_FIELDS_TRAILING:
        STRIPPED = MEAS_BLOCK.strip()
        DATA_FIELDS.append(STRIPPED)
        print("- " + STRIPPED)
 
print("\n======================================================================================\n")

#Since we cant risk having this program chew up like gigs of space, we can just delete our ghetto format
#CSV File and read from the live log through afterburner.
print("Removing original CSV and switching to low disk use methods...")
os.remove(CSV_OUTPUT)
try:
    os.remove(PATH_LOCATION)
    print("\nDeleted log file and continuing...")
except WindowsError:
    print("\nHOLD YOUR HORSES THERE BUD. YOU AINT NO ADMIN.")
    print("DIDNT WE GO OVER THIS LI7KE 30 SECONDS AGO?")
    print("RUN AGAIN AS A GODDAMN ADMIN WHY IS THAT SO HARD")

print("Pulling measurements now....")
time.sleep(1) #Used to let RTSS or AB write a new data point

with open(PATH_LOCATION) as RAW_MEAS_BLOCKS:
    VALUE_READER = csv.reader(RAW_MEAS_BLOCKS)
    for SKIP_COUNT in range(10):
        next(VALUE_READER)
    RAW_ROW = next(VALUE_READER)
    VALUES_RAW = RAW_ROW[2:]
    VALUES_CLEAN = []
    for RAW_VALUES in VALUES_RAW:
        STRIPPED = RAW_VALUES.strip()
        VALUES_CLEAN.append(STRIPPED)

print("\n======================================================================================\n")

print("Displaying recorded values now....")
PAIRED_DATA = zip(DATA_FIELDS, VALUES_CLEAN)

for PAIRS in PAIRED_DATA:
    print(PAIRS)

print("\n======================================================================================\n")

