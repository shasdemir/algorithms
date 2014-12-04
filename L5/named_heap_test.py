# test module for NamedHeap object

import unittest
from L5 import *
#from ps5_1_heapq import *


class NamedTests(unittest.TestCase):
    def test_up_heapify(self):
        heap = NamedHeap(heap_list=zip([2, 4, 3, 5, 9, 7, 7], ['a', 'b', 'c', 'd', 'e', 'f', 'g']))

        heap.heap_list.append((1, 'h'))
        heap.value_map['h'] = 1
        heap.position_map['h'] = len(heap.heap_list) - 1

        heap.__up_heapify__(-1)

        assert (1, 'h') == heap.heap_list[0]
        assert (2, 'a') == heap.heap_list[1]

    def test_dijkstra(self):
        # shortcuts
        (a, b, c, d, e, f, g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        triples = ((a, c, 3), (c, b, 10), (a, b, 15), (d, b, 9), (a, d, 4), (d, f, 7), (d, e, 3),
                   (e, g, 1), (e, f, 5), (f, g, 2), (b, f, 1))
        G = {}
        for (i, j, k) in triples:
            make_link(G, i, j, k)

        dist = dijkstra(G, a)

        assert dist[g] == 8  # (a -> d -> e -> g)
        assert dist[b] == 11  # (a -> d -> e -> g -> f -> b)

    def test_dijkstra_2(self):
        (a, b, c, d, e, f, g) = (0, 1, 2, 3, 4, 5, 6)
        triples = ((a, b, 2), (a, c, 2), (a, d, 4), (a, e, 2), (a, f, 4), (b, g, 5), (c, d, 4), (d, e, 1))
        G = {}
        for (i, j, k) in triples:
            make_link(G, i, j, k)

        assert dijkstra(G, a)[d] == 3  # a -> e -> d

    def test__dijkstra_3(self):
        (a, b, c, d) = ('A', 'B', 'C', 'D')
        triples = ((a, b, 1), (a, c, 4), (a, d, 4), (b, c, 1), (c, d, 1))
        G = {}
        for (i, j, k) in triples:
            make_link(G, i, j, k)

        dist = dijkstra(G, a)

        assert dist[d] == 3  # (a -> b -> c -> d)


if __name__ == '__main__':
    unittest.main()