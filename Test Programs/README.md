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

### PyWebTelem_IdleTemps.py (Work in progress)
- NOTE: THIS IS A WIP
- Program used to show how we can grab idle temps from the log file.
- We create a dynamic dictionary file that can be read and use it as a lookup for other info.
- The idea here is that we can scan the dictionary, see where the identifier of X usage is, and then from there we can lookup where the identifier of X usage is.  Given those two indicies, we can pull a usage value and a temperature.  
- Using a threshold value of usage, we can set this up to only read the temp of X component when the usage of X component is less than a set number.
- In other words:
    - Find out what's being monitored.
    - Create a list of pairs as INDEX, VALUE_RECORDED
    - Read the items in each index of the dictionary/list
    - When we come across the one that has the word usage in it we look at it's index.
    - If we see GPU also, we use 30 for a threshold. If we see CPU we use 15.
    - We then read the value of VALUES_CLEAN at the index marked by the dictionary and compare it to the threshold.
        - If we're under the threshold, we look at the dictionary again and find the temperature index of the component who's usage we're checking. 
        - That temp is now the idle temp.
        - If we're over the threshold, we ignore it. 

### PyWebTelem_DataTransmission.py (Work in progress)
- NOTE: This is a WIP and the file may be empty in the repo. 
- Program used to demonstrate data sending and receiving over using python. 
- Won't be pulling data from a log file, but instead just sending the contents of a list
- No graphing, no GUI, all console based still.
- Written as a try/except for the event that data supplied is impossible (Not supplied data or invalid data.)