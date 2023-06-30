import time
import math

def search_and_move(age, length, base, lower_bound):

    # Declare a list to use when converting the current age to a new base.
    converted_age = []
    
    # Convert the current age into the new base.
    while age > 0:
        converted_age.insert(0, age % base)
        age //= base

    # If the converted age has less digits than the current age, it must be smaller. Reduce the high search limit.
    if len(converted_age) < length:
        return (-1, base)
    
    # If the converted age has more than or equal digits, we must examine it.
    else:
        if max(converted_age) <= 9:                                 # If there are no invalid digits in the converted age,
            for i in range(len(converted_age)):                     # convert the values into string characters, so they can be joined
                converted_age[i] = str(converted_age[i])            # into one single number.
            age = int("".join(converted_age))
            if age >= lower_bound:                                  # If that number is greater than or equal to the lower bound, 
                return (0, base)                                    # return it to record the highest base found so far.
            else:
                return (-1, base)                                   # If it is less than the lower bound, reduce the high search limit.
        
        flag = True                                                 # Set a flag to know which way to reduce the search limit.
        numbers_correct = True                                      # Set a flag to track if the numbers seen so far are valid and correct.
        for i in range(1, length + 1):
            x = (lower_bound // pow(10, length - i)) % 10           # Isolate the digits in the lower bound number       
            last_digit = (i == length)                              # The last digit in the iterable.
            digits_match = (converted_age[i - 1] == x)              # The current digit in the lower bound and converted age list are both equal.
            current_digit_higher = (converted_age[i - 1] > x)       # The current age digit is higher than the current lower bound digit.
            current_digit_lower = (converted_age[i - 1] < x)        # The current age digit is lower than the current lower bound digit.
            invalid_digit = (converted_age[i - 1] > 9)              # The current age digit is not between 0 - 9.


            # Set the rules for moving the search limit up or down.
            if invalid_digit:                                       
                if numbers_correct:
                    flag = True
                    break
                else:
                    if last_digit:
                        flag = False
                        break
                    else:
                        flag = True
                        break
            elif numbers_correct:
                if current_digit_lower:
                    flag = False
                    break
                if current_digit_higher:
                    numbers_correct = False
                    continue
                elif digits_match:                                  
                    continue

        if flag:
            return(1, base)                         # If the flag is True, increase the low search limit.
        else:
            return(-1, base)                        # Else, reduce the high search limit.
        

def main():

    y, l = 0, 0                                     # Declare the variables for age and lower bound
    b = 10                                          # Track the highest valid base seen in the program. 
    valid = False                                   # Set valid to False to allow while loop to start.

    # Request input from user.
    while not valid:
        user_input = input("Age, Lower Bound: ")
        user_input = user_input.split()

        # Convert input to integer variables.
        try:
            y = int(user_input[0])
            l = int(user_input[1])
        except:
            print("INVALID USER INPUT - PLEASE TRY AGAIN.")
            continue

        # Check to see if the user input it valid within the rules.
        valid = (10 <= y <= 10**18) and (10 <= l <= y)

        # If user input is invalid, prompt user to repeat.
        if not valid:
            print("INVALID USER INPUT - PLEASE TRY AGAIN.")


    length = int(math.log10(l) + 1)                                 # Set the length of the lower bound number
    low = 10                                                        # Set the low search limit.
    high = y                                                        # Set the high search limit.
    
    # Start the clock to time the function
    start = time.time()

    # Initiate a binary search.
    while low <= high:                                          
        mid = (low + high) // 2                                     # Find the middle of the search range.
        movement, base = search_and_move(y, length, mid, l)         # Determin which way to continue the search.
        if movement == 0:                                           # If a 0 is returned, this is a match - record the current highest base found.
            b = base
            low = base + 1
        elif movement < 0:                                          # If a value less than 0 is returned, reduce the high search limit.
            high = base - 1
        else:
            low = base + 1                                          # If a value less than 0 is returned, increase the low search limit.
    

    # Print the result of the highest base found.
    print(b)
    duration = time.time() - start
    print("Runtime:", duration, "Seconds")

    return

main()