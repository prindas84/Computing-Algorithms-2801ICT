import numpy
import random
import time

def fold_card(R, C, Y, card):

    allowed = (1<=R<=50000) and (2<=C<=10**5) and (R * C <= 10**5) and (1<=Y<=C-1)
    if not allowed:
        print("The input values are out of scope.")
        return
    else:
        # If the fold is in the middle of a card with even columns...
        if C % Y == 0 and C / 2 == Y:
            for row in range(R):
                x = 1
                # Compare the elements in the first half of the list to their corrosponding index in the second half.
                for col in range(Y):
                    # If the elements are the same, print their value.
                    if card[row][col] == card[row][-x]:
                        print(card[row][col], end = '')
                    # Else, print closed because they do not match and can't be open.
                    else:
                        print('x', end = '')
                    x += 1
                print()

        # If there are overhanging columns from the original left...
        elif Y > C // 2:
            start = Y - (C % Y)
            for row in range(R):
                # Print the overhanging elements from the left.
                for col in range(start):
                    print(card[row][col], end = '')
                x = 1
                # For the remaining elements...
                # Compare the elements in the first half of the list to their corrosponding index in the second half.
                for col in range(start, start + ((C - start) // 2)):
                    # If the elements are the same, print their value.
                    if card[row][col] == card[row][-x]:
                        print(card[row][col], end = '')
                    # Else, print closed because they do not match and can't be open.
                    else:
                        print('x', end = '')
                    x += 1
                print()

        # If there are overhanging columns from the original right...
        else:
            end = C - (Y * 2)
            for row in range(R):
                # Print the overhanging elements from the left.
                for col in range(C - 1, C - end - 1, -1):
                    print(card[row][col], end = '')
                x = end + 1
                # For the remaining elements...
                # Compare the elements in the first half of the list to their corrosponding index in the second half.
                for col in range((C - end) // 2):
                    # If the elements are the same, print their value.
                    if card[row][col] == card[row][-x]:
                        print(card[row][col], end = '')
                    # Else, print closed because they do not match and can't be open.
                    else:
                        print('x', end = '')
                    x += 1
                print()
    return

def main():

    # Main vairable assignment.
    options = ['o', 'x']
    R = 10
    C = 10**4
    Y = 3
    card = numpy.array([[random.choice(options) for col in range(C)] for row in range(R)])    

    # Hardcoded test variables to confirm the correct results are being populated.
    R1 = 4
    C1 = 7
    Y1 = 3
    card1 =   [['o','x','o','o','o','x','o'],
               ['x','o','x','x','o','o','x'],
               ['x','x','x','o','x','x','o'],
               ['x','o','o','o','x','o','x']]
    
    R2 = 3
    C2 = 3
    Y2 = 1
    card2 =   [['o','x','x'],
               ['x','o','x'],
               ['x','x','o']]
    
    R3 = 3
    C3 = 3
    Y3 = 2
    card3 =   [['o','x','x'],
               ['x','o','x'],
               ['x','x','o']]
    
    R4 = 2
    C4 = 3
    Y4 = 1
    card4 =   [['o','o','x'],
               ['x','o','o']]
    

    # Start the clock to time the function
    start = time.time()

    # Main vairable function call.
    fold_card(R, C, Y, card)

    # Function calls for the test variables above.
    #fold_card(R1, C1, Y1, card1)
    #fold_card(R2, C2, Y2, card2)
    #fold_card(R3, C3, Y3, card3)
    #fold_card(R4, C4, Y4, card4)
    duration = time.time() - start
    print("Runtime:", duration, "Seconds")
    return

main()