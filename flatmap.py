#!/usr/bin/env python
# run with "python flatmap.py"
import unittest

# short and sweet
def flat_map_recursive_1(list_of_lists: list) -> list:
	flattened = []
	for item in list_of_lists:
		if isinstance(item, list):
			flattened.extend(flat_map_recursive_1(item))
		else:
			flattened.append(item)
	return flattened


# More in the direction of tail-call-optimized, which I found out too late doesn't make any difference in Python
def flat_map_recursive_2(list_of_lists: list) -> list:
	# base case: empty list
	if len(list_of_lists) < 1:
		return []

	# second case: list of length 1
	# if it's a list of lists, flatten it, otherwise return the list of one item.
	if len(list_of_lists) == 1:
		if isinstance(list_of_lists[0], list):
			return flat_map_recursive_2(list_of_lists[0])
		else:
			return list_of_lists

	# induction case: repeat on the list for indices 0 to n
	# if element 0 is a list, flatten it then append the rest of the list
	if isinstance(list_of_lists[0], list):
		return flat_map_recursive_2(list_of_lists[0]) + (flat_map_recursive_2(list_of_lists[1:]))
	else:
		return [list_of_lists[0]] + flat_map_recursive_2(list_of_lists[1:])

# iterative to prevent recursion limit/overflow
def flat_map_iterative(list_of_lists: list) -> list:
	for index, item in enumerate(list_of_lists):
		while index < len(list_of_lists) and isinstance(list_of_lists[index], list):
			list_of_lists[index:index + 1] = list_of_lists[index]
	return list_of_lists



class TestFlatMapMethods(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(flat_map_recursive_1([]), [])
        self.assertEqual(flat_map_recursive_2([]), [])
        self.assertEqual(flat_map_iterative([]), [])

    def test_flat(self):
    	test_input = [1,2,3]
    	expected = [1,2,3]
    	self.assertEqual(flat_map_recursive_1(test_input), expected)
    	self.assertEqual(flat_map_recursive_2(test_input), expected)
    	self.assertEqual(flat_map_iterative(test_input), expected)

    def test_nested(self):
    	test_input = [1, [2,3], 4, [5, [6], 7]]
    	expected = [1,2,3,4,5,6,7]
    	self.assertEqual(flat_map_recursive_1(test_input), expected)
    	self.assertEqual(flat_map_recursive_2(test_input), expected)
    	self.assertEqual(flat_map_iterative(test_input), expected)

    # creates a list of 800-deep nested lists
    def test_large(self):
    	test_input = [1]
    	for _ in range(800):
    		test_input[0] = [test_input[0]]
    	expected = [1]
    	self.assertEqual(flat_map_recursive_1(test_input), expected)
    	self.assertEqual(flat_map_recursive_2(test_input), expected)
    	self.assertEqual(flat_map_iterative(test_input), expected)

    # this causes the recursion limit to be exceeded with recursive solutions; only iterative works.
    def test_really_large(self):
        test_input = [1]
        for _ in range(1000000):
        	test_input[0] = [test_input[0]]
        expected = [1]
        self.assertEqual(flat_map_iterative(test_input), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
