#PyWebTelem V0.1
#Zack Walsh
#Python 2.7
#Built for use with Windows 10 and 8.1 using MSI AFB or RTSS

#NOTE: I added the error exception.  Just makes more sense.

#Here_We_Go.gif has started:

#Setup imports and explain why.
import os #Path searches
import csv #CSV and HML reading/writing
from collections import defaultdict #Parsing and saving collumn names
import time #Delays to stop the program from pulling stale/invalid values.

#Welcome Screen and splash
print("======================================================================================\n")
print("\t\t\t      PyWebTelemetry V1.0\n\t      This program NEEDS MSI Afterburner installed to work!")
print("\t       RivaTuner MIGHT also work, but I have not tested it")
print("\nStart Afterburner, right click the graphs on the bottom and click \"Log to file\".")
print("Once started, enter the log file location INCLUDING the file name.")
print("Default Path: \"C:/Program Files (x86)/MSI Afterburner/HardwareMonitoring.hml\n")
print("    THIS PROGRAM *MUST* BE RUN AS AN ADMIN IF YOUR LOG IS OUTSIDE YOUR USER FOLDER")
print("======================================================================================\n")

#Log file locating sequence
VALID_PATH = 0 #BOOLEAN. 0 = no path/bad path.  1 = path given/file confirmed real.
DEFAULT_PATH = 'C:/Program Files (x86)/MSI Afterburner/HardwareMonitoring.hml' #ProgFiles default

while VALID_PATH != 1:
    print("Enter the log file location using \'/\'. (Leave blank for default)")
    PATH_LOCATION = raw_input("Path: ") #Capture the path here
    
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

#Log file parsing to get measurements 
print("======================================================================================\n")
print("Opening file and start parse now....")

CSV_OUTPUT = 'CSV_OUTPUT.csv' #This file is temporary!!!!
print("\nFinding user desired measurments. This is a one time process!!")

print("Cleaning up extra lines...") #Write the tmep file
with open(PATH_LOCATION, "rb") as INPUT: #Open the log file and call it the input
    INPUT.next() #Since the logs are always going to have two lines of bs, skip.
    INPUT.next()
    with open(CSV_OUTPUT, "w") as OUTPUT: #Write OUTPUT file.
        CSV_WRITTER = csv.writer(OUTPUT) #CSV Writer begins
        for row in csv.reader(INPUT): #For each row in the input file...
            CSV_WRITTER.writerow(row[2:]) #Write said row BEGINING AFTER THE 2ND
            

print("Determining wanted measurements...") #Read the temp file
with open(CSV_OUTPUT) as UNSORTED:
    SORTER = csv.DictReader(UNSORTED, delimiter =',')
    DATA_FIELDS_TRAILING = SORTER.fieldnames #Fieldnames is just collumn names
    DATA_FIELDS = [] #Empty list for the measurement blocks
    print("\n\t\tMeasurement Blocks")
    for MEAS_BLOCK in DATA_FIELDS_TRAILING: #Print them out in a neat order.
        STRIPPED = MEAS_BLOCK.strip()
        DATA_FIELDS.append(STRIPPED)
        print("- " + STRIPPED)

print("\n======================================================================================\n")

#Delete all logs and CSV files now to save disk space then go into a loop.
print("Removing original CSV and switching to low disk use methods...")
os.remove(CSV_OUTPUT) #Remove the output file
try: #Check if we can modify the log file.  If not make the user try again as admin.
    os.remove(PATH_LOCATION)
    print("\nDeleted log file and continuing...")
except WindowsError:
    print("\nHOLD YOUR HORSES THERE BUD. YOU AINT NO ADMIN.")
    print("DIDNT WE GO OVER THIS LI7KE 30 SECONDS AGO?")
    print("RUN AGAIN AS A GODDAMN ADMIN WHY IS THAT SO HARD")

print("\n======================================================================================\n")
print("Printing measurements to console now....")

while True: #Loop for as long as we want.
    time.sleep(1) #Let AFB rewrite the log.
    try: #Added the error exception anyway. Didn't want to but it's just smarter.
        with open(PATH_LOCATION) as RAW_MEAS_BLOCKS: #open the log and read it.
            VALUE_READER = csv.reader(RAW_MEAS_BLOCKS)
            for SKIP_COUNT in range(10): #Skip 10 lines for the first recorded value.
                next(VALUE_READER)
            RAW_ROW = next(VALUE_READER)
            VALUES_RAW = RAW_ROW[2:] #Read all values after second collumn
            VALUES_CLEAN = [] #Place to store whitespace less values.
            for RAW_VALUES in VALUES_RAW:
                STRIPPED = RAW_VALUES.strip()
                VALUES_CLEAN.append(STRIPPED)

        #Zip the two lists together for easier reading.
        PAIRED_DATA = zip(DATA_FIELDS, VALUES_CLEAN)
        print(PAIRED_DATA)
        os.remove(PATH_LOCATION) #Delete the log and repeat.
    except: #Exception is just going to tell the user there's an issue.  No point in breaking.
        print("PULLED TOO FAST RETRYING")
        continue