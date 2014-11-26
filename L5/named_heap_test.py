# test module for NamedHeap object

import unittest
from L5 import NamedHeap

class NamedTests(unittest.TestCase):
    def test_up_heapify(self):
        heap = NamedHeap(heap_list=[2, 4, 3, 5, 9, 7, 7], heaped_names=['a'] * 7)

        heap.heap_list.append(1)

        heap.__up_heapify__(7)

        assert 1 == L[0]
        assert 2 == L[1]