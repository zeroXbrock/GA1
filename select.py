# select.py
# selects kth smallest element given m files containing n elements

import binascii
import os

# Start of operations		Done
def fn(m, n, k):
    # tracker vars
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

    # make list of file pointers
    for f in range(1,10):
		if(os.path.exists("./" + str(f) + ".dat")):
			inputFiles.append("./" + str(f) + ".dat")
			i += 1
			if(i == m):
				f = 10

    val = rec(m, n, k, begin, end, index, inputFiles)
    writeOutput(val)

#Done?
# return number at index i in file pointed to by fp
def getnum(i, fp):
	fp.seek(4 * i)
	return int(binascii.hexlify(fp.read(4)),16)

#Done
def getfp(filename):
    return open(filename, "rb")


#IDK
# search for n in file pointed to by fp
# return index of element equal to or nearest but less than n
def binSearch(num, fp, hi, low):
    loc = low + (hi - low) / 2
    current = getnum(loc, fp)

    print "num: " + str(num)
    print "hi: " + str(hi)
    print "low: " + str(low)
    print "curr: " + str(current)

    if (hi == low):
        print "1"
        return loc
    elif (current <= num and getnum(loc+1, fp) <= num):
        print "2"
        return binSearch(num, fp, hi, loc+1)
    elif (current <= num and getnum(loc+1, fp) > num):
        print "3"
        return loc
    elif (current > num):
        print "4"
        return binSearch(num, fp, loc, low)
    else:
        print "SHIT"
        return -1
    print "LAST"
    return -1

#Done
def lenSub(m, beg, end):
    return end[m] - beg[m] + 1

#IDK
def rec(m,n,k,beg,end,index,inputFiles):
    # Truncate arrays to length k
    for i in range(m):
        if (lenSub(i,beg,end) > k):
            end[i] = beg[i] + k

    # 0-based index of current largest file
    currSub = 0
    # Get the largest subarray
    for i in range(m):
        if (lenSub(currSub,beg,end) < lenSub(i,beg,end)):
            currSub = i

    # pick middle element of largest array
    currfp = getfp(inputFiles[currSub])
    mid = getnum(((lenSub(currSub, beg, end) - 1)/ 2), currfp) # val of mid el't
    index[currSub] = lenSub(currSub,beg,end) / 2

    for i in range(0,m):
        print "i: HERE " + str(i) + " " + str(m)
        mfile = getfp(inputFiles[i])
        if i != currSub and lenSub(i,beg,end) > 0:
            bsval = binSearch(mid, mfile, end[i], beg[i])
            index[i] = bsval
            print "bsval: " + str(bsval)

    # calculate L
    L = 0
    endcase = True
    for i in range(m):
        if (lenSub(i,beg,end) > 1):
            L += index[i]
            endcase = False

    # compare L w/ k
    #1
    if (k == 1):
        for i in range (m):
            if lenSub(i,beg,end) > 0:
                val = beg[i]
                break
        for i in range(m):
            if (lenSub(i,beg,end) > 0 and val > beg[i]):
                val = beg[i]
        #return val
        print "k==1"
        return getnum(val, currfp)
    #2
    elif (L == k):
        val = -1
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                if (end[i] > val):
                    val = end[i]
        #return val
        print "L==k"
        return getnum(val, currfp)
    #3
    elif (endcase == True):
        karr = []
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                karr.append(beg[i])
            return sorted(karr)[k]
    #4
    elif (L > k):
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                end[i] = index[i]
        return rec(m,n,k,beg,end,index,inputFiles)
    #5
    elif (L < k):
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                beg[i] = index[i] + 1
        return rec(m,n,k-L,beg,end,index,inputFiles)

#IDK
def readinput():
    with open('input.txt') as f:
        return (f.readline()).split(',')

#IDK
def writeOutput(num):
    with open('output.txt', 'w') as f:
        f.write(str(num))
        f.close()


#Done

#Reads in from input.txt
invars = readinput()
m = int(invars[0])
n = int(invars[1])
k = int(invars[2])

#Starts operations
fn(m, n, k)
