"""
Author: Jevan Smith, and Isaac Davidson
Assignment: Project4
Date: May 1, 2019
Description: Computes the Knapsack Problem a variety of ways.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import math


class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None

    def getValue(self, i, j):
        node = self
        prevNode = node
        while node is not None:
            if node.value[0] == i and node.value[1] == j:
                return node.value[2]
            prevNode = node
            node = node.next
        return prevNode.value[2]

    def insert(self, value):
        node = self
        prevNode = node  # Init previous node
        newNode = LinkedList(value)
        while node is not None:  # Traverse through list
            prevNode = node  # Saves previous node
            node = node.next
        prevNode.next = newNode


class HashTable:
    def __init__(self, k, bn, bw):
        self.size = k
        self.bn = bn
        self.bw = bw
        self.table = [None for x in range(k)]

    def insert(self, i, j, value):
        hash = self

        ri = bin(i)[2:].zfill(self.bn)
        rj = bin(j)[2:].zfill(self.bw)
        rij = int('1' + ri + rj, 2)
        pos = rij % hash.size

        zippedArray = []
        zippedArray.append(i)
        zippedArray.append(j)
        zippedArray.append(value)

        if hash.table[pos] is None:
            createLinkedList = LinkedList(zippedArray)
            hash.table[pos] = createLinkedList
        else:
            hash.table[pos].insert(zippedArray)

    def search(self, i, j):
        hash = self

        ri = bin(i)[2:].zfill(self.bn)
        rj = bin(j)[2:].zfill(self.bw)
        rij = int('1' + ri + rj, 2)
        pos = rij % hash.size

        if hash.table[pos] is None:
            return 0
        elif i == 0 or j == 0:  # since no zero row/col, return 0
            return 0
        else:
            return hash.table[pos].getValue(i, j)


def maxHeapify(list, i):
    """
    INPUT: list is an array which holds density/item values per element
    while i is an iterator value
    DESC: this function takes a list of tuples and max heapifies the given
    list of tuples, based on i its position within the heap.
    """
    greatest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < len(list) and list[left][0] > list[i][0]:
        greatest = left
    if right < len(list) and list[right][0] > list[greatest][0]:
        greatest = right
    if greatest != i:
        temp = list[i]
        list[i] = list[greatest]  # Swap
        list[greatest] = temp
        maxHeapify(list, greatest)


def deleteMax(list):
    """
    INPUT: list is an array which holds density/item values per element
    DESC: this function deletes the max key value from the heap
    RETURN: returns the max density value deleted, and item value associated to
    max density.
    """
    maxDensity = list[0][0]
    itemValue = list[0][1]
    list[0] = list[len(list)-1]
    list.pop()
    maxHeapify(list, 0)
    return maxDensity, itemValue


def maxHeap(densities, items):
    """
    INPUT: takes a list of densities and items
    DESC: this function combines densities/items into one list,
    and builds a maxHeap based on densities.
    RETURN: returns the value key value deleted
    """
    combine = list(zip(densities, items))
    n = len(combine)
    for i in range(n//2, -1, -1):
        maxHeapify(combine, i)
    return combine


def fileToList(cName, vName, wName):
    """
    INPUT: cName, vName, and wName are file names
    DESC: Takes file names and converts contents of file
    to a list of integers.
    RETURN: cArray, vArray, and wArray are all lists of ints
    """

    cArray = []
    vArray = []
    wArray = []
    chunk = ''

    for line in open(cName):
        for char in line:
            if char != '\n':
                chunk += char
        cArray.append(int(chunk))
        chunk = ''  # reset chunk

    for line in open(vName):
        for char in line:
            if char != '\n':
                chunk += char
        vArray.append(int(chunk))
        chunk = ''  # reset chunk

    for line in open(wName):
        for char in line:
            if char != '\n':
                chunk += char
        wArray.append(int(chunk))
        chunk = ''  # reset chunk

    return cArray, vArray, wArray


def dpApproach(c, v, w):
    """
    INPUT: c, v, and w are lists of integers
    DESC: Takes lists of integers and computes the knapsack problem
    using the dynamic programming approach.
    RETURN: optimal value as int, and the optimal subset
    """

    wSize = c[0]+1
    hSize = len(w)+1
    k = wSize * hSize

    v.insert(0, 0)
    w.insert(0, 0)
    table = [[0 for x in range(wSize)] for y in range(hSize)]  # initialize list

    for i in range(1, hSize):
        for j in range(1, wSize):
            if j-w[i] >= 0:
                value = max(table[i-1][j], v[i] + table[i-1][j-w[i]])
            else:
                value = table[i-1][j]
            table[i][j] = value

    result = table[hSize-1][wSize-1]
    subset = []
    i = hSize - 1
    j = wSize - 1

    while i > 0 and j > 0:
        if table[i][j] > table[i-1][j]:
            subset.append(i)
            j -= w[i]
        i -= 1

    return result, subset, k


def HashDpApproach(c, v, w):
    """
    INPUT: c, v, and w are lists of integers
    DESC: Takes lists of integers and computes the knapsack problem
    using the a heap dynamic programming approach.
    RETURN: optimal value as int, and the optimal subset
    """

    wSize = c[0]+1
    hSize = len(w)+1
    v.insert(0, 0)
    w.insert(0, 0)
    k = (wSize*hSize)//2

    bn = math.ceil(math.log2(hSize + 1))
    bw = math.ceil(math.log2(wSize + 1))
    hash = HashTable(k, bn, bw)

    for i in range(1, hSize):
        for j in range(1, wSize):
            if j-w[i] >= 0:
                value = max(hash.search(i-1, j), v[i] + hash.search(i-1, j-w[i]))
            else:
                value = hash.search(i-1, j)
            hash.insert(i, j, value)

    result = hash.search(hSize-1, wSize-1)
    subset = []
    i = hSize - 1
    j = wSize - 1

    while i > 0 and j > 0:
        if hash.search(i, j) > hash.search(i-1, j):
            subset.append(i)
            j -= w[i]
        i -= 1

    return result, subset, k


def greedyApproach(c, v, w):
    """
    INPUT: c, v, and w are lists of integers
    DESC: Takes lists of integers and computes the knapsack problem
    using the Greedy Approach approach.
    RETURN: optimal value as int, and the optimal subset
    """

    density = []
    items = []
    subset = []
    result = 0
    total = 0

    for i in range(len(v)):
        density.append(v[i]/w[i])
        items.append(i)

    n = len(items)

    sortedList = sorted(zip(density, items))
    sortedList.reverse()  # Reverse list descending order

    for i in sortedList:
        subset.append(items[i[1]]+1)
        total += w[i[1]]
        result += v[i[1]]
        if total > c[0]:
            subset.pop()
            total -= w[i[1]]
            result -= v[i[1]]
            return result, subset, n

    return result, subset, n


def maxGreedyApproach(c, v, w):
    """
    INPUT: c, v, and w are lists of integers
    DESC: Takes lists of integers and computes the knapsack problem
    using a max-heap Greedy Approach approach.
    RETURN: optimal value as int, and the optimal subset
    """

    density = []
    items = []
    subset = []
    result = 0
    total = 0

    for i in range(len(v)):
        density.append(v[i]/w[i])
        items.append(i)

    n = len(items)

    sortedList = maxHeap(density, items)

    for i in range(len(sortedList)):
        deleteValues = deleteMax(sortedList)
        subset.append(deleteValues[1]+1)
        total += w[deleteValues[1]]
        result += v[deleteValues[1]]
        if total > c[0]:
            subset.pop()
            total -= w[deleteValues[1]]
            result -= v[deleteValues[1]]
            return result, subset, n

    n = len(items)

    return result, subset, n


def main():

    print("==============================")
    print("MENU:")
    print("==============================")
    print("[1]: Task 1 and Task 2")
    print("[2]: Task 3")
    print("==============================")
    x = input("Option: ")
    print("")

    if x == '1':
        print("*Note: including .txt within the name")
        cFile = input("Enter file name for c: ")
        vFile = input("Enter file name for v: ")
        wFile = input("Enter file name for w: ")
        print("")

        listValues = fileToList(cFile, vFile, wFile)

        c = listValues[0]
        v = listValues[1]
        w = listValues[2]

        c1 = list(c)
        v1 = list(v)
        w1 = list(w)

        c2 = list(c)
        v2 = list(v)
        w2 = list(w)

        start = time.perf_counter()  # Start time
        dpResult = dpApproach(c, v, w)
        end = time.perf_counter()  # End time

        opValue = dpResult[0]
        opSubset = dpResult[1]

        opSubset.sort()

        print("Knapsack capacity =", c[0], "Total number of items =", len(v)-1)
        print("")
        print("Traditional Dynamic Programming Optimal value:", opValue)
        print("Traditional Dynamic Programming Optimal subset:", opSubset)
        print("Traditional Dynamic Programming Time Taken:", "%.2gs" % (end-start))
        print("")

        start = time.perf_counter()  # Start time
        hashDpResult = HashDpApproach(c1, v1, w1)
        end = time.perf_counter()  # End time

        opValue = hashDpResult[0]
        opSubset = hashDpResult[1]

        opSubset.sort()

        print("Space-efficient Dynamic Programming Optimal value:", opValue)
        print("Space-efficient Dynamic Programming Optimal subset:", opSubset)
        print("Space-efficient Dynamic Programming Time Taken:", "%.2gs" % (end - start))
        print("")

        start = time.perf_counter()  # Start time
        greedyResult = greedyApproach(c2, v2, w2)
        end = time.perf_counter()  # End time

        opValue = greedyResult[0]
        opSubset = greedyResult[1]

        opSubset.sort()

        print("Greedy Approach Optimal value:", opValue)
        print("Greedy Approach Optimal subset:", opSubset)
        print("Greedy Approach Time Taken:", "%.2gs" % (end-start))
        print("")

        start = time.perf_counter()  # Start time
        maxGreedyResult = maxGreedyApproach(c2, v2, w2)
        end = time.perf_counter()  # End time

        opValue = maxGreedyResult[0]
        opSubset = maxGreedyResult[1]

        opSubset.sort()

        print("Heap-based Greedy Approach Optimal value:", opValue)
        print("Heap-based Greedy Approach Optimal subset:", opSubset)
        print("Heap-based Greedy Approach Time Taken:", "%.2gs" % (end-start))

    else:
        timeValues1 = []
        timeValues2 = []
        timeValues3 = []
        timeValues4 = []
        spaceValues1 = []
        spaceValues2 = []
        nValues1 = []
        nValues2 = []
        for i in range(8):

            cValue = 'p0'+str(i)+'_c.txt'
            vValue = 'p0'+str(i)+'_v.txt'
            wValue = 'p0'+str(i)+'_w.txt'

            listValues = fileToList(cValue, vValue, wValue)

            c = listValues[0]
            v = listValues[1]
            w = listValues[2]

            c1 = list(c)
            v1 = list(v)
            w1 = list(w)

            c2 = list(c)
            v2 = list(v)
            w2 = list(w)

            start = time.perf_counter()  # Start time
            dpResult = dpApproach(c, v, w)
            end = time.perf_counter()  # End time

            timeValues1.append(end - start)
            spaceValues1.append(math.log2(dpResult[2]))

            start = time.perf_counter()  # Start time
            hashDpResult = HashDpApproach(c1, v1, w1)
            end = time.perf_counter()  # End time

            timeValues2.append(end - start)
            spaceValues2.append(math.log2(hashDpResult[2]))

            start = time.perf_counter()  # Start time
            greedyResult = greedyApproach(c2, v2, w2)
            end = time.perf_counter()  # End time

            timeValues3.append(end - start)
            nValues1.append(greedyResult[2])

            start = time.perf_counter()  # Start time
            maxGreedyResult = maxGreedyApproach(c2, v2, w2)
            end = time.perf_counter()  # End time

            timeValues4.append(end - start)
            nValues2.append(maxGreedyResult[2])

        plt.plot(spaceValues1, timeValues1, 'bs')
        plt.plot(spaceValues2, timeValues2, 'ro')
        plt.axis([0, 20, 0, 0.01])
        blue_patch = mpatches.Patch(color='blue', label="Dynamic Programming")
        red_patch = mpatches.Patch(color='red', label='Space-efficient Dynamic P.')
        plt.legend(handles=[red_patch, blue_patch])
        plt.title("Dynamic Programming Graph")
        plt.xlabel('space')
        plt.ylabel('time')
        plt.show()

        plt.plot(nValues1, timeValues3, 'bs')
        plt.plot(nValues2, timeValues4, 'ro')
        plt.axis([0, 20, 0, 0.0001])
        blue_patch = mpatches.Patch(color='blue', label="Greedy approach (in-built sort)")
        red_patch = mpatches.Patch(color='red', label='Greedy approach (max-heap)')
        plt.legend(handles=[red_patch, blue_patch])
        plt.title("Greedy approach Graph")
        plt.xlabel('n')
        plt.ylabel('time')
        plt.show()


if __name__ == "__main__":
    main()
