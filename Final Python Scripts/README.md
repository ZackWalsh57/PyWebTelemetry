# Final Python Scripts
- Any and all final code or scripts are found here. All versions (Even old releases) will be kept here and act as a changelog. 
- Any major changes will be documented under the headder for each version uploaded.

--- 

## Version 0.1
- Version 0.1 is the first stable build of the underlying code in this project.
- Features and Changes:
    - Reading a log file in .hml format
    - Auto detecting measurement blocks from the log
    - Console only output for now.
    - No web interface
    - ADDED: Error exception for when the program runs faster than AFB and tries to read another line of data before the log is rewritten
    - ADDED: Loop while true for continious data logging. 

## Version 0.1.1
- Added Min and Max logging.
- The program logs the values as floats instead of type String since string comparison is pointless in this program. 
- Averages are not included. See the file Averages Bug under the Test Programs folder for more info.