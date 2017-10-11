# select.py
# selects kth smallest element given m files containing n elements



#////////////////////////////////////////////////
#////////////////////////////////////////////////
#////////////////////////////////////////////////
#Done = Does what it is suppose to do

#Done? = With a quick glance it does what it is suppose to do

#IDK = It was way to fucking late to actually check so idk if actaully does what it suppose to do
#////////////////////////////////////////////////
#////////////////////////////////////////////////
#////////////////////////////////////////////////











import binascii
import os
import sys


#Done
# Start of operations
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
    for f in range(1,11):
        if(os.path.exists("./" + str(f) + ".dat")):
            inputFiles.append("./" + str(f) + ".dat")
            i += 1
            if(i == m):
                f = 10

    val = rec(m, n, k, begin, end, index, inputFiles)           #returns a number into val
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




def lenSub(m, beg, end):
    return end[m] - beg[m] + 1




def rec(m,n,k,beg,end,index,inputFiles):

    #Done
    # Truncate arrays to length k
    for i in range(m):
        if (lenSub(i,beg,end) > k):
            end[i] = beg[i] + k

    # for i in range(m):
    #     print "beg: " + str(beg[i]) + " end: " + str(end[i])
    #     print "index: " + str(index[i])

    #Done
    # 0-based index of current largest file
    currSub = 0
    # Get the largest subarray
    for i in range(m):
        if ( lenSub(currSub,beg,end) < lenSub(i,beg,end) ):
            currSub = i
            print "CurrSub: " + str(lenSub(currSub,beg,end))
        else:
            print "Small: " + str(lenSub(i, beg, end))


    #Done?
    # pick middle element of largest array
    currfp = getfp(inputFiles[currSub])

    #SO WE NEED TO KEEP DOING ^^^^^^






    index[currSub] = ((beg[currSub] + end[currSub])) / 2

    mid = getnum(index[currSub], currfp)  # val of mid el't
    print "Curr-index: " + str(index[currSub])

    #Done?
    for i in range(0,m):
        #print "i: " + str(i) + " m: " + str(m) + " n: " + str(n) + " k: " + str(k) + " "
        mfile = getfp(inputFiles[i])
        if i != currSub and lenSub(i,beg,end) > 0:
            bsval = binSearch(mid - 1, mfile, end[i], beg[i])        #added -1 so recheck my work This is correct! (or should be)
            index[i] = bsval
            #print "bsval: " + str(bsval)
            mfile.close()


    #Done

    # calculate L
    L = 0
    endcase = True
    for i in range(m):
        if (lenSub(i, beg, end) > 1):  # if elements left is 0 or 1
            endcase = False
        if (lenSub(i,beg,index) > 0):     #CHANGED 1 -> 0 ........................... what.............
            if index[i] > -1:
                L += lenSub(i,beg,index)    #DON'T GRAB INDEX HERE.... LENGTH FROM BEG TO INDEX
            if (lenSub(i,beg,end) > 1):     #if elements left is 0 or 1
                endcase = False


    print "L: " + str(L)
    #
    # if L == 0:
    #     for i in range(m):
    #         mfile = getfp(inputFiles[i])
    #         print " " + str(i) + "=" + str(getnum(index[i], mfile))
    #         mfile.close()



    #IDK

    # compare L w/ k
    #1

    #CHECK UR GODDAMN currfp!!!!!!!!!!!!!!!!!
    #Done?
    if (k == 1):
        print "k==1"
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

    #2 Base case for 
    elif (L == k):
        print "L==k"
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


    #4 Base Case for recursion
    elif (L > k):
        print "L > K"
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                end[i] = index[i]
        currfp.close()
        print str(k)

        for i in range(m):
            print "beg: " + str(beg[i]) + " end: " + str(end[i])
            print "index: " + str(index[i])

        return rec(m,n,k,beg,end,index,inputFiles)


    #5 Base Case for recursion
    elif (L < k):
        print "L < K"
        for i in range(m):
            if (lenSub(i,beg,end) > 0):
                if index[i] >= 0:
                    beg[i] = index[i] + 1

        currfp.close()
        print str(k-L)

        for i in range(m):
            print "beg: " + str(beg[i]) + " end: " + str(end[i])
            print "index: " + str(index[i])

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
