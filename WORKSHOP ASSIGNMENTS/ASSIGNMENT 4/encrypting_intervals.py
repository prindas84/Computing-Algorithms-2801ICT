import math
import time

def calculate_relative_count(a, b, c, d):

	# Set the low and high value of the entire range. Initialise the count to 0.
	low = min(a, c)
	high = max(b, d)
	count = 0

	# Initialise a set to store the relatively prime combinations. Set the count to 0.
	relatively_prime = set()

	# Find a list of all prime numbers in range(a,b), range(c,d) and a boolean array of all prime numbers in the entire range.
	prime_numbers_one = find_prime_list(max(2, a), b)
	prime_numbers_two = find_prime_list(max(2, c), d)
	prime_range = find_prime_range(max(2, low), high)

	# To save time, find the count of all relatively prime combinations involving the value 1. Then set 1 to 2 to remove duplicates later.
	if a == 1:
		count += d - c + 1
		a = 2
	if c == 1:
		count += b - a + 1
		c = 2
	if a == 1 and c == 1:
		count -= 1

	# Add all combinations (P, N) where P is prime in list A and N is less than P in list B. 
	counter = 1
	for i in range(len(prime_numbers_one) - 1, -1, -1):
		while prime_numbers_one[i] - counter in range(c, d + 1):
			relatively_prime.add((prime_numbers_one[i], prime_numbers_one[i] - counter))
			counter += 1

	# Add all combinations where A and B are consecutive numbers.	
	for i in range(a, b + 1):
		if (i + 1) in range(c, d + 1):
			relatively_prime.add((i, i + 1))
		if ((i - 1) > 1) and ((i - 1) in range(c, d + 1)):
			relatively_prime.add((i, i - 1))

	# Add all combinations where at least one number is prime, and the other is not a multiple of itself.
	for i in range(len(prime_numbers_one)):
		current_prime_one = prime_numbers_one[i]
		for j in range(c, d + 1):
			if (current_prime_one != j) and ((current_prime_one % j != current_prime_one) or (j % current_prime_one != 0)):
				relatively_prime.add((current_prime_one, j))
	for i in range(a, b + 1):
		for j in range(len(prime_numbers_two)):
			current_prime_two = prime_numbers_two[j]
			if (i != current_prime_two) and ((i % current_prime_two != i) or (current_prime_two % i != 0)):
				relatively_prime.add((i, current_prime_two))

	# Add all composite number combinations where the GCD is equal to 1.
	for i in range(max(2, a), b + 1):
		# If the number in the first list is prime, it can't be composite. SKIP.
		if prime_range[i]:
			continue
		# If number in the first list is even...
		if i % 2 == 0:
			# If first number in the second list is even, start at the next position and skip all even numbers.
			if c % 2 == 0:
				for j in range(c + 1, d + 1, 2):
					# If the number in the second list is prime, it can't be composite.
					# If the combination of I and J are a multiple of 5 or 10, they can't be relative primes. SKIP. 
					if prime_range[j] or (i % 10 == 0 and c % 5 == 0):
						continue
					# If the combination of I and J are not already in the relative primes set, check the GCD.
					elif (i, j) not in relatively_prime:
						if gcd(i, j) == 1:
							relatively_prime.add((i, j))
			# If first number in the second list is odd, start at the first position and skip all even numbers.
			else:
				for j in range(c, d + 1, 2):
					# If the number in the second list is prime, it can't be composite.
					# If the combination of I and J are a multiple of 5 or 10, they can't be relative primes. SKIP. 
					if prime_range[j] or (i % 10 == 0 and c % 5 == 0):
						continue
					# If the combination of I and J are not already in the relative primes set, check the GCD.
					elif (i, j) not in relatively_prime:
						if gcd(i, j) == 1:
							relatively_prime.add((i, j))
		# If the number in the first list is odd, traverse the second list as normal.
		else:
			for j in range(c, d + 1):
				# If the number in the second list is prime, it can't be composite.
				# If the combination of I and J are a multiple of 5 or 10, they can't be relative primes. SKIP. 
				if prime_range[j] or (i % 5 == 0 and c % 10 == 0):
					continue
				# If the combination of I and J are not already in the relative primes set, check the GCD.
				elif (i, j) not in relatively_prime:
					if gcd(i, j) == 1:
						relatively_prime.add((i, j))

	# Return the number of combinations in the relative prime set, as well as the initial count of combination involving the value 1.
	return count + len(relatively_prime)


def find_prime_base(high):

	"""	REFERENCE: https://www.geeksforgeeks.org/segmented-sieve-print-primes-in-a-range/ 
		I have made some alterations, however I borrowed the main concepts from this website. """
	
	base_numbers = []                                   # Initialise a list to store the base prime numbers under the high limit of sqrt(high)
	n = int(math.sqrt(high))							# Find the sqrt(high) to be the limit to stop the search.
	valid_primes = [True for i in range(n + 1)]			# Initialise boolean array of all numbers to the high limit.
	
	
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
		I have made some alterations, however I borrowed the main concepts from this website. """
	
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


def find_prime_range(low, high):

	"""	REFERENCE: https://www.geeksforgeeks.org/segmented-sieve-print-primes-in-a-range/ 
		I have made some alterations, however I borrowed the main concepts from this website. """
		
	# Find the base prime numbers required to complete the required calculations.
	base_numbers = find_prime_base(high)

	# Initialise boolean array of all numbers between the low - high limit.
	prime_range = [True for i in range(high + 1)]
	prime_range[0], prime_range[1] = False, False

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
			prime_range[j] = False

	return prime_range


def gcd(a, b):

	""" This function will find the Greatest Common Divisor between two integers. """

	# Set the divisor as the largest number of the two.
	divisor = a
	if b > a:
		divisor = b
	
	# Loop down from the largest number until a common divisor is found, then return it.
	for i in range(divisor, -1, -1):
		if (a % i == 0) and (b % i == 0):
			return i
	
	return 1


def user_input():

	a, b, c, d = 0, 0, 0, 0

	# Request first input from the user.
	valid = False
	while not valid:
		user_input = input("INPUT (A, B): ")
		user_input = user_input.split()

		# Convert input to integer variables.
		try:
			a = int(user_input[0])
			b = int(user_input[1])
		except:
			print("INVALID USER INPUT - PLEASE TRY AGAIN.")
			continue

		# Check to see if the user input it valid within the rules.
		valid = (1 <= a <= b <= 10**4) and (b - a <= 10**4)

		# If user input is invalid, prompt user to repeat.
		if not valid:
			print("INVALID USER INPUT - PLEASE TRY AGAIN.")

	# Request second input from the user.
	valid = False
	while not valid:
		user_input = input("INPUT (C, D): ")
		user_input = user_input.split()

		# Convert input to integer variables.
		try:
			c = int(user_input[0])
			d = int(user_input[1])
		except:
			print("INVALID USER INPUT - PLEASE TRY AGAIN.")
			continue

		# Check to see if the user input it valid within the rules.
		valid = (1 <= c <= d <= 10**4) and (d - c <= 10**4)

		# If user input is invalid, prompt user to repeat.
		if not valid:
			print("INVALID USER INPUT - PLEASE TRY AGAIN.")

	return (a, b, c, d)


def main():

	# Get the user input for the program.
	a, b, c, d = user_input()

	# Start the clock timer.
	start = time.time()

	# Initiate the calculation.
	count = calculate_relative_count(a, b, c, d)

	# Print the result.
	print(count)

	# Stop the clock.
	duration = time.time() - start
	print("Runtime:", duration, "Seconds")

	return


main()

