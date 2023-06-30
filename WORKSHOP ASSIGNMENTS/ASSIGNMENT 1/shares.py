import time

# Input the number of days to calculate the total shares with - HARCODED
days = 10**12
shares = days

# Start the clock to time the function
start = time.time()

# Begin the calculation at the second day, as we have already assigned the first day allocation to the count above.
i = 2
while i < days:
    # If a point is reached where we can make a jump, add the number of shares within the jump section to the total count.
    if (days // (days // i)) != i:
        skip = ((days // (days // i)) + 1) - i
        shares += (days // i) * skip
    # Else, add the next number of shares from a single calculation.
    else:
        shares += days // i
    # Increment i accordingly
    i = (days // (days // i)) + 1

print("Total Shares:", shares)
duration = time.time() - start
print("Runtime:", duration, "Seconds")