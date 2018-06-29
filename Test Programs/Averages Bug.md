# Average Calculation Bug:

- Calculate the Average for each indexed value by adding to itself and dividing by the itteration counter
   - BUG: This method may not work.... It seems as though it is averaging the previous average and the next seen value.  
   - The average of 5,10,5,15 assuming there are 4 itterations = 8.75
   - The average of 8.75 and the next value of 10 at 5 itterations = 3.75
   - The average of 5,10,5,15,10 at 5 itterations = 9.0
   - If this was going to work, all of the averages should be the same.
- The program should work like this:
    - It needs to take all of the vlaues it's seen in the past and add them. THEN divide by the itterations.
    - The problem I'm going to have is that the sum of all the previous values may cause me an overflow error.
    - So for now, the averages will be disabled. I could update them less frequently but then I don't have an  accurate number.  
    
# This is the Code I Wanted to Use:
    AVERAGE_SUM = 0
    while True:
        ITTERATIONS = 0 #Loop Counter
        INDEX_PLACE = 0 #List index tracker.

        ....
        
        # The code above and under this is for finding the values, mins, and maxes from the logs.
        
        ....
        
        while INDEX_PLACE < len(CLEAN_VALUES):
            for VALUE in CLEAN_VALUES:
                AVERAGES[INDEX_PLACE] = ((AVERAGES[INDEX_PLACE] + VALUE) / ITTERATIONS)
                
                #This was going to be used as an overall counter but it would become massive.
                AVERAGE_SUM += VALUE 
                
                INDEX_PLACE += 1

            if INDEX_PLACE = len(CLEAN_VALUES):
                
                #INDEX_PLACE is reset to prevent an error for an index out of range.

                INDEX_PLACE = 0


- The problem I ran into this way is that the average calculated is not real unless we can summate every single previous run.
- This is because for each average, the next added value is weighted less and less, but summing it all up would reach system maxsize of a 32 bit os really fast.  So I'm not sure how to make this work. 