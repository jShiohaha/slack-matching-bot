import unittest
import importlib

# external package imports
from pprint import pprint

# local project imports 
from src.match import *
from .constants import *

# coverage run -m tests.test
# coverage html
# open htmlcov/index.html

''' COMPLETELY NEW GRAPH '''
class TestNewGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tests.constants
        importlib.reload(tests.constants)

    def test_one_match_for_two_people(self):
        num_matches, matches = generate_matches(TWO_INDIVIDUALS, None)
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(matches), 1)

    def test_one_match_for_three_people(self):
        num_matches, matches = generate_matches(THREE_INDIVIDUALS, THREE_MEMBER_ONE_MATCH)
        self.assertEqual(num_matches, 1)
        # matches contain pair-wise matches and unmatched people 
        self.assertEqual(len(matches), 2)

    def test_one_match_for_four_people(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, FOUR_MEMBERS_ONE_MATCHES)
        self.assertEqual(num_matches, 1)
        # matches contain pair-wise matches and unmatched people 
        self.assertEqual(len(matches), 3)

    def test_two_matches_for_four_people(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, FOUR_MEMBERS_TWO_MATCHES)
        self.assertEqual(num_matches, 2)
        self.assertEqual(len(matches), 2)

    def test_matches_for_four_people(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, None)
        self.assertEqual(num_matches, 2)
        self.assertEqual(len(matches), 2)

    def test_matches_for_five_people(self):
        # passing None invokes creation of a complete graph
        num_matches, matches = generate_matches(FIVE_INDIVIDUALS, None)
        self.assertEqual(num_matches, 2)
        self.assertEqual(len(matches), 2)

    def test_matches_for_n_people(self):
        n = len(NAMES) # assuming n is even
        g = build_graph(NAMES, graph=None)
        # passing None invokes creation of a complete graph
        num_matches, matches = generate_matches(NAMES, g)

        self.assertEqual(num_matches, int(n/2))
        self.assertEqual(len(matches), int(n/2))

    def test_matches_for_n_plus_one_people(self):
        n = len(NAMES) # assuming n is even

        names_copy = list(NAMES)
        names_copy.append(OTHER_NAME)
        g = build_graph(names_copy, graph=None)
        # passing None invokes creation of a complete graph
        num_matches, matches = generate_matches(names_copy, g)

        # one group of 3 should exist
        self.assertTrue(3 in [len(match) for match in matches])
        self.assertEqual(num_matches, int(n/2))
        self.assertEqual(len(matches), int(n/2))


''' GROUPINGS NOT POSSIBLE '''
class TestNoMatches(unittest.TestCase):
    def test_no_match_for_no_people(self):
        num_matches, matches = generate_matches([], None)
        self.assertEqual(num_matches, -1)
        self.assertEqual(len(matches), 0)

    def test_no_match_for_one_person(self):
        num_matches, matches = generate_matches(ONE_INDIVIDUAL, None)
        self.assertEqual(num_matches, 0)
        self.assertEqual(len(matches), 1)

    def test_no_matches_for_four_people(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, build_empty_graph(FOUR_INDIVIDUALS))
        self.assertEqual(num_matches, 0)
        self.assertEqual(len(matches), 4)


''' NEW MEMBERS JOIN '''
class TestNewMembersAdded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tests.constants
        importlib.reload(tests.constants)

    def test_matches_add_one_person_for_two_people_total(self):
        num_matches, matches = generate_matches(TWO_INDIVIDUALS, build_empty_graph(ONE_INDIVIDUAL))
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(matches), 1)

    def test_matches_add_two_people_for_three_people_total(self):
        num_matches, matches = generate_matches(THREE_INDIVIDUALS, build_empty_graph(ONE_INDIVIDUAL)) 
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(matches), 1)

    def test_matches_add_one_person_for_three_people_total(self):
        num_matches, matches = generate_matches(THREE_INDIVIDUALS, build_empty_graph(TWO_INDIVIDUALS))
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(matches), 1)

    # TODO: this situation will generate 2 unmatched people... do we want this?
    def test_matches_add_two_people_for_four_people_total(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, build_empty_graph(TWO_INDIVIDUALS))
        self.assertEqual(num_matches, 2)
        self.assertEqual(len(matches), 2)

    def test_matches_add_one_person_for_four_people_total_when_one_existing_match_possible(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, THREE_MEMBER_ONE_MATCH)
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(matches), 2)

    def test_matches_add_one_person_for_four_people_total_when_one_existing_match_possible_unsorted_dict_by_possible_matches(self):
        # THREE_MEMBER_ONE_MATCH_ALT is unsorted graph, update_graph function should fix this
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, THREE_MEMBER_ONE_MATCH_ALT)
        self.assertEqual(num_matches, 2)
        self.assertEqual(len(matches), 2)

    def test_matches_add_one_person_for_four_people_total(self):
        num_matches, matches = generate_matches(FOUR_INDIVIDUALS, build_empty_graph(THREE_INDIVIDUALS))
        self.assertEqual(num_matches, 1)
        self.assertEqual(len(matches), 2)

    def test_matches_add_odd_people_for_even_people_total(self):
        total_people_possible = 10
        names_copy = list(NAMES[:total_people_possible])
        n = len(names_copy)

        # names includes the first member; the same person who the empty graph is based off
        num_matches, matches = generate_matches(names_copy, build_empty_graph(ONE_INDIVIDUAL))
        self.assertEqual(num_matches, n/2)
        self.assertEqual(len(matches), n/2)

    def test_matches_add_even_people_for_odd_people_total(self):
        total_people_possible = 9
        names_copy = list(NAMES[:total_people_possible])
        n = len(names_copy)

        # names includes the first member; the same person who the empty graph is based off
        num_matches, matches = generate_matches(names_copy, build_empty_graph(ONE_INDIVIDUAL))
        self.assertEqual(num_matches, (n-1)/2)
        self.assertEqual(len(matches), (n-1)/2)

    def test_matches_add_n_people_total(self):
        n = len(NAMES)
        # names includes the first member; the same person who the empty graph is based off
        num_matches, matches = generate_matches(NAMES, build_empty_graph(ONE_INDIVIDUAL))
        self.assertEqual(num_matches, n/2)
        self.assertEqual(len(matches), n/2)


if __name__ == '__main__':
    unittest.main()