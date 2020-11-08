"""The Magic Triangle"""

import csv
import sys

def rotate(card, count):
	"""Rotate a card CCW (neg. values) or CW (pos. values) in multiples 
	of 120 degrees.

	rotate((1,2,3), -2) -> (3,1,2)
	rotate((1,2,3),  2) -> (2,3,1)

	Rotations:

		count = 0           1           2
		        (no rot.)   (120 deg)   (240 deg)
		        *
		       / \         / \         / \  
		      /   \       /   \       /   \ 
		     /     \     /     \     /     \
		     -------     -------*   *-------"""

	# Convert CCW rotations (neg. values) to equivalent CW rotations
	# (avoids problems with negative indices)
	n = len(card)
	while count < 0:
		count += n
	
	rotated = [0] * len(card)
	for i in range(n):
		rotated[(i + count) % n] = card[i]

	return tuple(rotated)


def shuffle_deck(config, deck):
	"""Shuffle the deck of cards as specified by the configuration c."""
	return [rotate(deck[c[0]], c[1]) if c is not None else None for c in config]


def is_solution(config, deck, partial=False):
	"""Returns true if the configuration is a valid solution, otherwise false. A pair of triangles
	match, if the body parts  printed on the neighboring sides of the triangles are complements 
	(head and body), i.e. if they are not equal, and if the colors are the same."""
	if config is None:
		print("config is None")
		return False

	shuffled_deck = shuffle_deck(config, deck)

	for edge in edge_matches:
		card0 = shuffled_deck[edge[0]]
		card1 = shuffled_deck[edge[1]]
		if None in [card0, card1]:
			if partial:
				continue
			else:
				return False

		# Reminder: body parts must be different while colors must match
		side = edge[2]
		side0 = card0[side]
		side1 = card1[side]
		# print "s0 = %s, s1 = %s " % (side0, side1) # Debug
		is_match = side0[0] != side1[0] and side0[1] == side1[1]
		if not is_match:
			return False

	return True


def output(config, deck):
	"""Returns string containing a configuration in a human-readablea form."""

	# Debug
	# s = ""
	# d = ""
	# labels = ('0a', '0b',  '0', '0c',
	# 	      '1c',  '1', '2a', '2b',
	# 	      '1b', '1a', '8a', '8b',
	# 	       '2',  '8', '2c', '8c',
	# 	      '3c', '6c',  '3',  '6',
	# 	      '4a', '4b', '3b', '3a',
	# 	      '5a', '5b', '6b', '6a',
	# 	      '7a', '7b',  '4',  '5',
	# 	       '7', '4c', '5c', '7c')
	s = shuffle_deck(config, deck)
	d = [card[0] for card in config]
	labels = (s[0][0], s[0][1], d[0],    s[0][2],
		      s[1][2], d[1],    s[2][0], s[2][1],
		      s[1][1], s[1][0], s[8][0], s[8][1],
		      d[2],    d[8],    s[2][2], s[8][2],
		      s[3][2], s[6][2], d[3],    d[6],
		      s[4][0], s[4][1], s[3][1], s[3][0],
		      s[5][0], s[5][1], s[6][1], s[6][0],
		      s[7][0], s[7][1], d[4],    d[5],
		      d[7],    s[4][2], s[5][2], s[7][2])

	triangle = """
                / \    
               /   \   
              /{} {}\  
             /   {}   \ 
            /    {}   \ 
            ----------- 
          / \    {}   / \     
         /   \   {}   /   \    
        /{} {}\{} {}/{} {}\   
       /   {}   \   /   {}   \ 
      /    {}   \ /    {}   \ 
      ----------- ----------- 
    / \    {}   / \    {}   / \     
   /   \   {}   /   \   {}   /   \    
  /{} {}\{} {}/{} {}\{} {}/{} {}\   
 /   {}   \   /   {}   \   /   {}   \ 
/    {}   \ /    {}   \ /    {}   \ 
----------- ----------- ----------- 
""".format(*labels)

	msg = "config = {}\ndeck   = {}\n{}".format(config, s, triangle)

	return msg


def first(config, deck):
	"""Generate a first extension of the current configuration; find the first empty element in the 
	configuration (None), which will be filled with the next free card. If no empty elements exist, 
	the return value will be None"""
	first_empty = next((i for i in range(len(config)) if config[i] is None), None)
	if first_empty is None:
		return None

	# Find the next free card that can be added to the configuration at the location determined 
	# above.
	new_config = config[:]
	used_cards = [card[0] for card in new_config if card is not None]
	for i in range(len(deck)):
		if i not in used_cards:
			new_config[first_empty] = (i, 0) # Add the i-th card, with no rotation (0)
			break

	return new_config


def next_config(config, deck):
	"""Returns the next possible configuration given the current configuration; will return None if 
	no next configuration exists."""
	first_empty = next((i for i in range(len(config)) if config[i] is None), len(deck))

	# Avoid negative indices
	last_non_empty = first_empty - 1
	if last_non_empty < 0:
		return None

	# Determine the next configuration. If possible, rotate the current
	# last card, otherwise choose and select a new card.
	new_config = config[:]
	current_card = config[last_non_empty][0]
	current_rotation = config[last_non_empty][1]
	if current_rotation < 2:
		new_config[last_non_empty] = (current_card, current_rotation + 1)
	else:
		# No next card exists, if the current card is the last card in
		# the deck. Abort the search.
		if current_card >= len(deck) - 1:
			return None

		# Determine the next possible card for testing; ignore all cards
		# that already have been tested before.
		used_cards = [card[0] for card in new_config if card is not None]
		for i in range(current_card, len(deck)):
			if i not in used_cards:
				new_config[last_non_empty] = (i, 0) # Add the i-th card, with no rotation (0)
				break
	
	# If the configuration didn't change until now, a next item doesn't
	# exist and that will be indicated by returning None.
	if new_config == config:
		return None

	return new_config


def backtrack(config, deck):
	"""Text-book backtracking, cf. https://en.wikipedia.org/wiki/Backtracking"""
	
	# Abort the search in the current subtree if the configuration isn't complete and edge tests 
	# already fail, otherwise false.
	if not is_solution(config, deck, partial=True):
		return

	if is_solution(config, deck):
		print(output(config, deck))

	cur = first(config, deck)
	while cur is not None:
		backtrack(cur, deck)
		cur = next_config(cur, deck)


def read_csv(filename):
	"""Read data from a CSV file. The return value is a list of lists of strings."""
	data = []
	with open(filename) as fd:
		f = filter(lambda row: row[0]!='#', fd)
		csv_reader = csv.reader(f, delimiter=',', quotechar='"', skipinitialspace=True)
		for row in csv_reader:
			data.append(row)

	return data


if __name__ == "__main__":
	# Read the set of the playing cards of the game and the set of checks required to determine 
	# valid solutions.
	deck = read_csv(sys.argv[1])
	edge_matches = [[int(j) for j in i] for i in read_csv(sys.argv[2])] # Convert str -> int
	assert len(deck) == 9 and len(edge_matches) == 9

	# Start the search.
	config = [None] * len(deck)
	backtrack(config, deck)
