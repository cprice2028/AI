import sys;args = sys.argv[1:]
import math
import time
pzls=open(args[0]).read().splitlines()

SIZE = 0
WIDTH = 0
HEIGHT = 0
LENGTH=0
SYMSET = []
CSET = []
CSETLOOKUP=[]
NBRS=[]

def setGlobals(pzl):
    global LENGTH,SIZE,WIDTH,HEIGHT,SYMSET,CSET,CSETLOOKUP,NBRS #makes the listed variables refer to the globals
    CSET=[]
    CSETLOOKUP=[]
    LENGTH = len(pzl)
    SIZE=int(math.sqrt(LENGTH))
    WIDTH,HEIGHT=dimensions(SIZE)
    syms=["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    '''if SIZE ==9:
        SYMSET = ["1","2","3","4","5","6","7","8","9"]
    elif SIZE ==12:
        SYMSET = ["1","2","3","4","5","6","7","8","9","A","B","C"]
    elif SIZE ==16:
        SYMSET = ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    else:'''
    SYMSET = syms[:SIZE]

    for r in range(SIZE):
        r_indices = [r * SIZE + c for c in range(SIZE)] #all indices of one row
        CSET.append(r_indices)
        
    for c in range(SIZE):
        c_indices = [r * SIZE + c for r in range(SIZE)] #all indices of one column
        CSET.append(c_indices)
        
    for block_row in range(0, SIZE, HEIGHT): #loop vertically through subblocks height
        for block_col in range(0, SIZE, WIDTH): # loop horizontally through subblocks width
            block_indices = [] #empty list to store indices of sublock
            for r in range(HEIGHT): #loop through each row and column of the subblock
                for c in range(WIDTH):
                    block_indices.append((block_row + r) * SIZE + block_col + c) #convert to normal index
            CSET.append(block_indices)

    CSETLOOKUP = [[] for _ in range(LENGTH)] #makes a lookup list, index returns a list of the three constraint sets pertaining to that index
    for constraint in CSET:
        for i in constraint:
            CSETLOOKUP[i].append(constraint)

    NBRS = [set() for _ in range(LENGTH)] # indices within the constraint of the position, not including itself
    for i in range(LENGTH):
        for constraint in CSETLOOKUP[i]:
            for ci in constraint:
                if ci != i:
                    NBRS[i].add(ci)
        NBRS[i] = list(NBRS[i])


def main():
    i=1
    for pzl in pzls:
        pzlstart=pzl
        start_time = time.time()
        setGlobals(pzl)
        pzl = bruteForce(pzl,0)
        end_time=time.time()
        elapsed=end_time-start_time
        if pzl:
            if i>9 and i<100:
                print(f" {i}: {pzlstart}")
                print(f"     {pzl} {checkSum(pzl)} {elapsed:.1f}s")
            elif i>99:
                print(f"{i}: {pzlstart}")
                print(f"     {pzl} {checkSum(pzl)} {elapsed:.1f}s")
            else:
                print(f"  {i}: {pzlstart}")
                print(f"     {pzl} {checkSum(pzl)} {elapsed:.1f}s")
        else:
            if i>9 and i<100:
                print(f" {i}: {pzlstart}")
                print(f"     No Solution {checkSum(pzl)} {elapsed:.1f}s")
            elif i>99:
                print(f"{i}: {pzlstart}")
                print(f"     No Solution {checkSum(pzl)} {elapsed:.1f}s")
            else:
                print(f"  {i}: {pzlstart}")
                print(f"     No Solution {checkSum(pzl)} {elapsed:.1f}s")
        i+=1

def checkSum(pzl):
    ascii_dict = {chr(i): i for i in range(48,91)}
    chars = [ascii_dict[c] for c in pzl]
    return sum(ascii_dict[c]-min(chars) for c in pzl) #checksum instructed sum

def dimensions(num: int):
    divisor = 1 #tracks the divisor
    factors=[] #list of factors

    while divisor <=num: # factors of a number must be less than or equal to the number, hence the while loop check
        quotient = num/divisor #gets the quotient of number and divisor
        if num%divisor==0: # checks if the quotient has decimal values of .0
            factors.append((int(quotient),divisor)) #appends the factors as a tuple of integer to the list
        divisor+=1 #increment divisor
    smallest_w,current_height=factors[0]

    for w,h in factors: #for factors in factor list
        if w>=h and w<smallest_w: #check if width is greater than or equal to height and if the width is smaller than the smallest width
            smallest_w=w #update the smallest width that is >= height
            current_height=h #updated the smallest width corresponding height

    return (smallest_w,current_height)#return tuple of the dimensions


def isInvalid(pzl):
    for constraint in CSET: #check all constraints
        seen = set()
        for i in constraint:  #for every index in a constraint set
            if pzl[i] != '.':
                if pzl[i] in seen:
                    return True     #duplicate found
                seen.add(pzl[i])
    return False                  

    
def filled(pzl):
    return "." not in pzl

def getGoodSymbols(pzl, idx):
    seen = {pzl[nbr] for nbr in NBRS[idx]} 
     #possible symbols for an index are all symbols that do not appear in the populated cells in the indices constraint set
    return [s for s in SYMSET if s not in seen] #remaining symbols

def findBestSymbol(pzl, pos, symbols):
    if len(symbols) <= 1:
        return symbols #only one possible symbol

    count = {symbol:0 for symbol in symbols}
    for i in NBRS[pos]:
        if pzl[i] != '.':
            continue
        seen = {pzl[k] for k in NBRS[i]} #one set per empty neighbor
        for symbol in symbols:
            if symbol not in seen:  #symbol could still be a neighbor of i
                count[symbol] += 1

    return sorted(symbols, key=count.get) #sorts symbols from least to most count, useful

def findBestPosition(pzl):

    numsymbols=len(SYMSET)
    bestidx = -1
    min_possible = len(SYMSET) + 1 
    smallest_symbols=SYMSET

    for i in range(LENGTH):
        if pzl[i] != '.': #filled cell
            continue
        seen = {pzl[nbr] for nbr in NBRS[i]}
        seen.discard('.')     #symbols that exist in the constraint neighbors
        n = numsymbols - len(seen)  

        if n < min_possible:
            min_possible = n
            bestidx = i
            best_seen = seen
            if n <= 1: #break, 1 possible symbol is the best possible
                break

    if bestidx == -1:
        return -1, SYMSET
    return bestidx, [s for s in SYMSET if s not in best_seen]

def bruteForce(pzl,n):
    if n==0 and isInvalid(pzl): #only need to do full board check on the first pass
        return ""

    if filled(pzl):
        return pzl

    nextEmptyIndex,possiblesymbols = findBestPosition(pzl) #find best position return the best position index adn possible symbols

    bestsymbols = findBestSymbol(pzl, nextEmptyIndex, possiblesymbols) #bestsymbols returns the symbols ordered by utility

    for symbol in bestsymbols: #collectivey exhaustive
        newpzl = pzl[:nextEmptyIndex] + symbol + pzl[nextEmptyIndex + 1:]
        res = bruteForce(newpzl,1) #there is no invalid check because in findBestPosition it return possible symbols which are guarenteed to pass the invalid check,avoids recomputation
        if res:
            return res

    return ""


if __name__ == "__main__":
    main()

# Charlie Price, pd 3, 2028