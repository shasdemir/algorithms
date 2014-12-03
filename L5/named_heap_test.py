# test module for NamedHeap object

import unittest
from L5 import *


class NamedTests(unittest.TestCase):
    def test_up_heapify(self):
        heap = NamedHeap(heap_list=[2, 4, 3, 5, 9, 7, 7], heaped_names=['a'] * 7)

        heap.heap_list.append(1)
        heap.heaped_names.append('a')

        heap.__up_heapify__(-1)

        assert 1 == heap.heap_list[0]
        assert 2 == heap.heap_list[1]

    def test_dijkstra(self):
        # shortcuts
        (a, b, c, d, e, f, g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        triples = ((a, c, 3), (c, b, 10), (a, b, 15), (d, b, 9), (a, d, 4), (d, f, 7), (d, e, 3),
                   (e, g, 1), (e, f, 5), (f, g, 2), (b, f, 1))
        G = {}
        for (i, j, k) in triples:
            make_link(G, i, j, k)

        dist = dijkstra(G, a)

        print "dist: %s" % dist

        assert dist[g] == 8  # (a -> d -> e -> g)
        assert dist[b] == 11  # (a -> d -> e -> g -> f -> b)


if __name__ == '__main__':
    unittest.main()