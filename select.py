#select.py
#Selects kth smallest element given m files containing n elements

import binascii
import os
import sys

#Start of operations
def fn(m, n, k):
    #Tracker vars
    begin = []  #Keeps track of the beginning of each array
    end = []    #Keeps track of the end of each array
    index = []  #Keeps track of the numbers we grabbing

    #Setting each array to size m
    for i in range(m):
        begin.append(0)
        index.append(0)
        if(k < n):
            end.append(k)
        else:
            end.append(n)

    inputFiles = []
    i = 0

    #Make list of file pointers
    for f in range(1,11):
        if(os.path.exists("./" + str(f) + ".dat")):
            inputFiles.append("./" + str(f) + ".dat")
            i += 1
            if(i == m):
                f = 10

    val = rec(m, n, k, begin, end, index, inputFiles)           #returns a number into val
    writeOutput(val)


#Return number at index i in file pointed to by fp
def getnum(i, fp):
    fp.seek(4 * i)
    return int(binascii.hexlify(fp.read(4)),16)


#Opens the file
def getfp(filename):
    return open(filename, "rb")


#Search for n in file pointed to by fp
#Return index of element equal to or nearest but less than n
def binSearch(elem, bpoint, high, low): #elem = mid - 1
    if low > high:
        return -2

    loc = (high - low) / 2
    loc += low
    current = getnum(loc, bpoint)

    if elem >= current:
        temp = binSearch(elem, bpoint, high, loc + 1)
        if temp == -2:
            return loc
        else:
            return temp
    elif elem < current:
        temp = binSearch(elem, bpoint, loc - 1, low)
        loc = -2
        if temp == -2:
            return loc
        else:
            return temp


#Length of subarray
def lenSub(m, beg, end):
    return end[m] - beg[m] + 1


#Recursive function that finds k and returns it
def rec(m,n,k,beg,end,index,inputFiles):

    # Truncate arrays to length k
    for i in range(m):
        if (lenSub(i,beg,end) > k):
            end[i] = beg[i] + k

    # 0-based index of current largest file
    currSub = 0
    # Get the largest subarray
    for i in range(m):
        if ( lenSub(currSub,beg,end) < lenSub(i,beg,end) ):
            currSub = i

    #Pick middle element of largest array
    currfp = getfp(inputFiles[currSub])
    index[currSub] = ((beg[currSub] + end[currSub])) / 2
    mid = getnum(index[currSub], currfp)  # val of middle of the subarray

    #Grab index for each subarray
    for i in range(0,m):
        mfile = getfp(inputFiles[i])
        if i != currSub and lenSub(i,beg,end) > 0:
            bsval = binSearch(mid - 1, mfile, end[i], beg[i])
            index[i] = bsval
            mfile.close()

    #Calculate L
    L = 0
    endcase = True
    for i in range(m):
        if (lenSub(i, beg, end) > 1):# if elements left is 0 or 1
            endcase = False
        if (lenSub(i,beg,index) > 0):
            if index[i] > -1:
                L += lenSub(i,beg,index)
            if (lenSub(i,beg,end) > 1):     #if elements left is 0 or 1
                endcase = False

    #1 Base case for the lowest value = k
    if (k == 1):
        print "K == 1"
        NewI = 0

        #Grab one array that isn't empty
        for i in range (m):
            if (lenSub(i,beg,end) > 0):
                val = beg[i]
                NewI = i
                break

        #Check the one array against the others
        for i in range(m):
            if (lenSub(i,beg,end) > 0 and val > beg[i]):
                val = beg[i]
                NewI = i
                
        currfp.close()
        currfp = getfp(inputFiles[NewI])

        return getnum(val, currfp)

    #2 Base case for the remaining elements equals k
    elif (L == k):
        print "L == K"
        NewI = 0
        val = -1

        for i in range(m):
            if (lenSub(i,beg,index) > 0):
                if (index[i] > val):
                    val = index[i]
                    NewI = i

        currfp.close()
        currfp = getfp(inputFiles[NewI])
        return getnum(val, currfp)

    #3 Base case for if every array has 0 or 1 elements
    elif (endcase == True):
        print "endcase == True"
        karr = []
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                currfp.close()
                currfp = getfp(inputFiles[i])
                karr.append(getnum(i, currfp))

        currfp.close()
        return sorted(karr)[k]


    #1 Recursion case: makes the end index much smaller
    elif (L > k):
        print "L > K"
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                end[i] = index[i]

        currfp.close()
        return rec(m,n,k,beg,end,index,inputFiles)


    #2 Recursion case: make k smaller and move the beg index
    elif (L < k):
        print "L < K"
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                if index[i] >= 0:
                    beg[i] = index[i] + 1

        currfp.close()
        return rec(m,n,k-L,beg,end,index,inputFiles)


#Reads in the input file
def readinput():
    with open('input.txt') as f:
        return (f.readline()).split(',')


#Writes to the output file
def writeOutput(num):
    with open('output.txt', 'w') as f:
        print "NUMBER: " + str(num)
        f.write(str(num))
        f.close()


#Start Here
#Reads in from input.txt
invars = readinput()
m = int(invars[0])
n = int(invars[1])
k = int(invars[2])

sys.setrecursionlimit(10000)

#Starts operations
fn(m, n, k)