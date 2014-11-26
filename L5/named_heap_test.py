# test module for NamedHeap object

import unittest
from L5 import NamedHeap

# class NamedTests(unittest.TestCase):
#     def test


def test_uh():
    L = [2, 4, 3, 5, 9, 7, 7]
    L.append(1)
    up_heapify(L, 7)
    assert 1 == L[0]
    assert 2 == L[1]