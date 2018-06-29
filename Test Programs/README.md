# Test Programs
Any programs that are used for testing single run logging are found here. 

### PyWebTelem_OneRun.py
- The first complied script which is confirmed working. Contains tons of comments and docs explaining what goes on in the program.
- Only grabs one measurement set (the final version loops over for continious logging)
- Does not send the data anywhere.  Only prints the zipped list to the console window and is not formatted.
- This program was modified slightly and published as version 0.1

### PyWebTelem_AvgMinMax.py
- Script written to show how we can monitor the values logged and find some values the user may find usefull.
- When run the program checks to see what is being monitored and finds the following values if possible:
    - Average CPU Temperature
    - Average GPU Temperature(s)
    - Average CPU Use
    - Average RAM Use
    - Average GPU Use (Applies for more than one card if wanted)
    - CPU Idle Temp (Estimated. Found by checking usage)
- This data will eventually be stored in a list as well and then sent over to the web server and displayed.
- This program is going to run concurrently alongside the data logging program.
- NOTE: The average feature does not work right now.

### PyWebTelem_DataTransmission.py (Work in progress)
- NOTE: This is a WIP and the file may be empty in the repo. 
- Program used to demonstrate data sending and receiving over using python. 
- Won't be pulling data from a log file, but instead just sending the contents of a list
- No graphing, no GUI, all console based still.
- Written as a try/except for the event that data supplied is impossible (Not supplied data or invalid data.)
