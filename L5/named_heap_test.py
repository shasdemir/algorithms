# test module for NamedHeap object

import unittest
from L5 import NamedHeap


class NamedTests(unittest.TestCase):
    def test_up_heapify(self):
        heap = NamedHeap(heap_list=[2, 4, 3, 5, 9, 7, 7], heaped_names=['a'] * 7)

        heap.heap_list.append(1)
        heap.heaped_names.append('a')

        heap.__up_heapify__(-1)

        print "heap.heap_list: %s" % heap.heap_list
        assert 1 == heap.heap_list[0]
        assert 2 == heap.heap_list[1]


if __name__ == '__main__':
    unittest.main()