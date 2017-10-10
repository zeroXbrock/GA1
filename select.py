import binascii
from binarytree import tree, show, inspect, bst

# adds ".dat" to whatever number you give i
# returns a string "i.dat"
def itof(i):
    return str(i)+".dat"

# gets nth number from file in decimal format
def getnum(n, filename):
    with open(filename, "rb") as f:
        f.seek(4*n)
        return int(binascii.hexlify(f.read(4)), 16)

# gets next available lowest number from a file given
# mi which contains index of smallest number
def getNextNum(f, mi):
    return getnum(mi[f], itof(f+1))

# m: number of files to read
# n: number of numbers to read from file
# k: (kth smallest) element to search for
def getk(m,n,k):
    c = []
    mi = []
    for i in range(m):
        mi.append(0)
    
    while len(c) < k:
        # temp; smallest available value from each file
        cc = []
        for f in range(m):
            cc.append(getNextNum(f, mi))
        for i in range(len(cc)):
            #print "i: " + str(i)
            if (cc[i] == min(cc)):
                c.append(cc[i])
                mi[i] = mi[i] + 1
                cc = []
                break
        
    # pick kth smallest element from one of all files
    return c[len(c)-1]

def readInput():
    with open("input.txt", 'r') as f:
        return (f.readline()).split(',')

def main():
    print "main"
    # read input file
    args = readInput()
    m = int(args[0])
    n = int(args[1])
    k = int(args[2])

    # get k
    print "finding k..."
    k = getk(m,n,k)
        
    # write k to output file
    with open("output.txt", "w") as of:
        of.write(str(k))

if __name__ == '__main__':
    main()
