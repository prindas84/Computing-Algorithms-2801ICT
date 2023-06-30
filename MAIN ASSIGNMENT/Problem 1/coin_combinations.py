import numpy as np
import time
import math

input_file_path = "C:\\Users\Griffith University\OneDrive - Griffith University\Desktop\Projects\Computing Algorithms\Assignment\Problem 1\Input.txt"
output_file_path = "C:\\Users\Griffith University\OneDrive - Griffith University\Desktop\Projects\Computing Algorithms\Assignment\Problem 1\Output.txt"


def calculate_combinations(total_owing, coins, coin_count, low_range, high_range):

	"""REFERENCE: Minh Hieu Nguyen assisted me with this function, in determining how to calculate the results table. """

	combination_count = 0

	# Initialise the ways matrix, and calculate the initial values when the coin value 1 is used.
	ways_matrix = {value: {n: 0 for n in range(total_owing + 1)} for value in range(0, total_owing + 1)}
	for value in range(total_owing + 1):
		number_of_coins_row = {n: 0 for n in range(total_owing + 1)}
		number_of_coins_row[value] = 1
		ways_matrix[value] = number_of_coins_row
	result_table = np.zeros((total_owing + 1, total_owing + 1))

	# Increment the number of ways per N coins used, using the values of the smaller problems already calculated.
	for coin_index in range(1, coin_count):
		coin_value = coins[coin_index]
		for current_value in range(1, total_owing + 1):
			if coin_value > current_value:
				continue
			else:
				for number_of_coins in range(len(ways_matrix[current_value - coin_value]) - 1):
					ways_matrix[current_value][number_of_coins + 1] += ways_matrix[current_value - coin_value][number_of_coins]

	# Convert the ways dictionary into a 2D array.
	for value, list_ways in ways_matrix.items():
		for ways in range(len(list_ways)):
			result_table[value][ways] = list_ways[ways]

	# Calculate the number of combinations within the range of coins being used.
	for k in range(low_range, high_range + 1):
		combination_count += result_table[total_owing][k]

	return combination_count


def find_prime_base(high):

	"""	REFERENCE: https://www.geeksforgeeks.org/segmented-sieve-print-primes-in-a-range/
		I have made some alterations, however I borrowed the main concepts from this website.
		I wrote this function  in the Week 8 Workshop - encrypting_intervals.py """

	base_numbers = []								# Initialise a list to store the base prime numbers under the high limit of sqrt(high)
	n = int(math.sqrt(high))						# Find the sqrt(high) to be the limit to stop the search.
	valid_primes = [True for i in range(n + 1)]		# Initialise boolean array of all numbers to the high limit.

	# Starting from i = 2, set all multiples of i - that are greater than i - to False (not a prime number).
	for i in range(2, n + 1):
		if valid_primes[i]:
			for j in range(i * i, n + 1, i):
				valid_primes[j] = False

	# Starting from index 2, loop the list to find all numbers below n that are set to True (are prime numbers).
	for k in range(2, n + 1):
		if valid_primes[k]:
			base_numbers.append(k)

	# Return the list of base prime numbers to continue the next calculations.
	return base_numbers


def find_prime_list(low, high):

	"""	REFERENCE: https://www.geeksforgeeks.org/segmented-sieve-print-primes-in-a-range/
		I have made some alterations, however I borrowed the main concepts from this website.
		I wrote this function  in the Week 8 Workshop - encrypting_intervals.py """

	# Find the base prime numbers required to complete the required calculations.
	base_numbers = find_prime_base(high)

	# Initialise boolean array of all numbers between the low - high limit.
	valid_primes = [True for i in range(high + 1)]

	# Starting from the first base prime number, set all multiples of i - that are greater than i - to False (not a prime number).
	for i in base_numbers:
		lower = (low // i)
		if lower <= 1:
			lower = i + i
		elif (low % i) != 0:
			lower = (lower * i) + i
		else:
			lower = lower * i
		for j in range(lower, high + 1, i):
			valid_primes[j - low] = False

	# Add all prime numbers to a list to be returned.
	prime_numbers = []

	for k in range(low, high + 1):
		if valid_primes[k - low]:
			prime_numbers.append(k)

	return prime_numbers


def initiate(input_line):

	""" This function will initiate the calculation for each input, depending on it's specifications. """

	total_owing, low_range, high_range = 0, 0, 0

	# If the input uses option 2 - two input integers (total value, number of coins to use)...
	if len(input_line) == 2:
		total_owing = input_line[0]
		low_range = input_line[1]
		high_range = input_line[1]

	# If the input uses option 3 - three input integers (total value, number of coins in a range to use)...
	elif len(input_line) == 3:
		total_owing = input_line[0]
		low_range = input_line[1]
		high_range = input_line[2]

	# If the input uses option 3 - one input integers (total value). If the input has an error in it, it will also use this setting.
	else:
		total_owing = input_line[0]
		low_range = 1
		high_range = total_owing

	# Find the list of coins to use, using the find prime list function.
	coins = find_prime_list(1, total_owing)

	# If the gold coin is not already included, add it to the coins list and determine the number of coins in the list.
	if total_owing not in coins:
		coins.append(total_owing)
	coin_count = len(coins)

	return calculate_combinations(total_owing, coins, coin_count, low_range, high_range)


def process_file():

	""" This function will open the file and return a list of all input values for each line. """

	global input_file_path
	input = []

	# Open the file at the path set in the global variables.
	try:
		# Open the input file.
		input_file = open(input_file_path, "r")
	except:
		# Display error if file does not open.
		print("ERROR: FILE NOT FOUND - PLEASE TRY AGAIN")

	# For each line in the file, read the line and add it to the list of inputs.
	while True:
		line = [int(x) for x in input_file.readline().split()]
		if len(line) == 0:
			break
		input.append(line)

	input_file.close()

	return input


def main():

	input = process_file()

	try:
		# Open the input file.
		output_file = open(output_file_path, "w")
	except:
		# Display error if file does not open.
		print("ERROR: FILE NOT CREATED - PLEASE TRY AGAIN")

	# Start the clock to time the function.
	global start_timer
	start_timer = time.time()

	# Calculate the combination count for each input value in the list and write it to the output file.
	for line in input:
		combination_count = initiate(line)
		duration = time.time() - start_timer
		output_file.write("Combinations: {:<20}Runtime: {} Seconds\n".format(int(combination_count), duration))
	
	print("PROGRAM COMPLETE...")

	output_file.close()

	return

main()