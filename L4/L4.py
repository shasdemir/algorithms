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

# for i in range(len(answer)):
#     print i, answer[i][1], "(", answer[i][0], ")"


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
        else:
            right.append(val)
    return left, [v], right


def top_k(L, k):
    v = random.choice(L)

    left, middle, right = partition(L, v)

    if len(left) == k:
        return left
    if len(left) + 1 == k:
        return left + [v]
    if len(left) > k:
        return top_k(left, k)
    if len(left) < k:
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
    minimum = L.pop(0)

    L[0], L[1:] = L[-1], L[:-1]  # move last element to the beginning
    down_heapify(L, 0)

    return L  # return minimum


def insert_heap(L, v):
    L.append(v)
    up_heapify(L, len(L)-1)