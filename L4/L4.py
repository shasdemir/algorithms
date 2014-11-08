import random


#            animal       speed   weight lifespan brain
#                          (mph)   (kg)  (years) mass (g)
animals = [("dog",          46,   35,     13,  280    ),
           ("elephant",     30, 3500,     50, 6250    ),
           ("frog",          5,    0.5,    8,    3    ),
           ("hippopotamus", 45, 1600,     45,  573    ),
           ("horse",        40,  385,     30, 642     ),
           ("human",        27,   80,     78, 2000    ),
           ("lion",         50,  250,     30,  454    ),
           ("mouse",         8,    0.025,  2,    0.625),
           ("rabbit",       25,    4,     12,   40    ),
           ("shark",        26,  230,     20,   92    ),
           ("sparrow",      16,    0.024,  7,    2    )]


def importance_rank(items, weights):
    names = [item[0] for item in items]  # get the list of animal names
    scores = [sum([a*b for (a,b) in zip(item[1:], weights)]) for item in items]  # get the list of overall scores for each animal
    results = zip(scores,names) # make a list of tuple
    res2 = sorted(results) # sort the tuple based on the score
    return res2

answer = importance_rank(animals, (2, 3, 7, 1))


def mean(L):
    return sum(L) / float(len(L))


def rank(L, v):
    pos = 0
    for val in L:
        if val < v:
            pos += 1
    return pos


def partition(L, v):
    left = []
    right = []
    for val in L:
        if val < v:
            left.append(val)
        elif v < val:
            right.append(val)
    return left, [v], right


def top_k(L, k):  # actually the smallest k
    v = random.choice(L)

    left, middle, right = partition(L, v)

    if len(left) == k:
        return left
    if len(left) + 1 == k:
        return left + [v]
    if len(left) > k:
        return top_k(left, k)
    else:
        return left + [v] + top_k(right, k - len(left) - 1)


left = lambda i: 2 * i + 1
right = lambda i: 2 * i + 2
parent = lambda i: (i - 1) // 2
is_root = lambda i: i == 0
is_leaf = lambda L, i: right(i) > len(L) and left(i) > len(L)
one_child = lambda L, i: right(i) == len(L)  # the node only has a left child


def down_heapify(L, i):
    """ Call this if the heap rooted at i satisfies the heap property except perhaps i to its immediate children. """

    if is_leaf(L, i):
        return L

    if one_child(L, i):
        if L[i] > L[left(i)]:
            L[i], L[left(i)] = L[left(i)], L[i]
            return L

    # i has two children, check heap property
    if min(L[left(i)], L[right(i)]) >= L[i]:
        return L

    # if that fails, swap with the smaller child, and recurse on its children
    if L[left(i)] < L[right(i)]:
        L[i], L[left(i)] = L[left(i)], L[i]
        down_heapify(L, left(i))
    else:
        L[i], L[right(i)] = L[right(i)], L[i]
        down_heapify(L, right(i))
    return L


def build_heap(L):
    for i in range(len(L)-1, -1, -1):
        down_heapify(L, i)
    return L


def remove_min(L):
    L[0] = L.pop()  # move last element to the beginning
    down_heapify(L, 0)

    return L


def insert_heap(L, v):
    L.append(v)
    up_heapify(L, len(L)-1)


def median(L):  # theta(n)
    lower_half = top_k(L, ((len(L)+1) / 2))
    return sorted(lower_half)[-1]


def minimize_absolute(L):
    return median(L)


def mode(L):
    counts = {}
    for item in L:
        if item not in counts:
            counts[item] = 1
        else:
            counts[item] += 1

    return sorted(counts.items(), key=lambda x: x[1])[-1][0]


def up_heapify(L, i):
    if i == 0 or L[parent(i)] <= L[i]:
        return L
    else:
        L[parent(i)], L[i] = L[i], L[parent(i)]
        return up_heapify(L, parent(i))


def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {node2: 1}
    elif node2 not in G[node1]:
        G[node1][node2] = 1
    else:
        G[node1][node2] += 1

    if node2 not in G:
        G[node2] = {node1: 1}
    elif node1 not in G[node2]:
        G[node2][node1] = 1
    else:
        G[node2][node1] += 1

    return G


def path(G, v1, v2):
    open_list = [v1]
    path_from_start = {v1: [v1]}

    if v1 == v2:
        return path_from_start[v1]

    while open_list:
        current = open_list.pop(0)  # bfs

        for neighbor in G[current]:
            if neighbor not in path_from_start:
                path_from_start[neighbor] = path_from_start[current] + [neighbor]
                if neighbor == v2:
                    return path_from_start[v2]
                open_list.append(neighbor)
    return False


def centrality(G, v):
    open_list = [v]
    distance_from_start = {v: 0}

    while open_list:
        current = open_list.pop(0)  # bfs

        for neighbor in G[current]:
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                open_list.append(neighbor)
    return sum(distance_from_start.values()) / float(len(distance_from_start))


def centrality_naive(G, v):
    path_lengths = [len(path(G, v, other))-1 for other in G]
    return sum(path_lengths) / float(len(G.keys()))