import networkx as nx
from itertools import islice
from networkx.classes.function import path_weight
import time

input_file_path = "C:\\Users\Griffith University\OneDrive - Griffith University\Desktop\Projects\Computing Algorithms\Assignment\Problem 2\input.txt"
output_file_path = "C:\\Users\Griffith University\OneDrive - Griffith University\Desktop\Projects\Computing Algorithms\Assignment\Problem 2\output.txt"


"""REFERENCE: Minh Hieu Nguyen assisted me with this problem by pointing me int he direction of the networkx library and its functioanlity. """

def find_shortest_paths(graph, source, destination, k):

	""" This function will find the K shortests paths in a graph, given a source and destination. """

	# Find the K shortest paths in the graph.
	k_paths = islice(nx.shortest_simple_paths(graph, source, destination, "weight"), k)
	paths = []
	distances = []

	# For each path, split it into a path and a distance, then append each to the relavant list. 
	for path in k_paths:
		paths.append(path)
		distances.append(path_weight(graph, path, weight="weight"))

	# Zip each path and distance together to be used in other functions.
	return zip(paths, distances)


def process_file():

	global input_file_path
	
	# Open the file at the path set in the global variables.
	try:
		# Open the input file.
		input_file = open(input_file_path, "r")
	except:
		# Display error if file does not open.
		print("ERROR: FILE NOT FOUND - PLEASE TRY AGAIN")

	# Create a directed graph with the networkx library.
	graph = nx.DiGraph()

	# Read the first line of the input file to find the number of paths contained in the file. 
	first_line = input_file.readline().split()
	m = int(first_line[1])

	# Iterate over each path in the file and add it to the graph. From Node -> To Node, then Distance Between.
	for i in range(m):
		from_node, to_node, distance = input_file.readline().split()
		graph.add_edge(from_node, to_node, weight=float(distance))

	# Read the final line in the graph to find the source, destination, and the value of K.
	source, destination, k = input_file.readline().split()
	
	return (graph, source, destination, int(k))


def output_results(paths_distances):

	global output_file_path
	global start_timer

	try:
		# Open the input file.
		output_file = open(output_file_path, "w")
	except:
		# Display error if file does not open.
		print("ERROR: FILE NOT CREATED - PLEASE TRY AGAIN")

	# Write the information to file.
	output_file.write("SHORTEST K PATHS:\n\n")

	i = 1
	for path, distance in paths_distances:
		output_file.write("PATH {}: {} -- TOTAL DISTANCE: {}\n".format(i, ', '.join(path), distance))
		i += 1

	duration = time.time() - start_timer
	output_file.write("\n\nRuntime: {} Seconds ".format(duration))

	return


def main():

	# Start the clock to time the function.
	global start_timer
	start_timer = time.time()

	# Process the file into a graph.
	graph, source, destination, k = process_file()

	# Find the paths and distances of the shortest K paths.
	paths_distances = find_shortest_paths(graph, source, destination, k)

	# Print the results to file.
	output_results(paths_distances)
	
	print("PROGRAM COMPLETE...")

	return

main()