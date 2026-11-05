import sys;args = sys.argv[1:]

def main():
    length = int(args[0])*int(args[0])
    width=int(args[0])
    pzl = ["." for _ in range(length)]

    for arg in args[1:]:
        index = int(arg[:-1])
        char = arg[-1]
        pzl[index]=char
    
    pzl="".join(pzl)

    pzl = bruteForce(pzl)

    if pzl:
        print("\n".join(pzl[i:i+width] for i in range(0, length, width)))
    else:
        print("No solution")


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


def invalid(pzl):
    width, height = int(args[0]),int(args[0])
    symbols = [chr(i + 65) for i in range(width)]

    for i in range(height):
        copysymbols = symbols.copy()
        for j in range(width):
            piece = pzl[i * width + j]
            if piece in copysymbols:
                copysymbols.remove(piece)
            elif piece != ".":
                return False

    for i in range(width):
        copysymbols = symbols.copy()
        for j in range(height):
            piece = pzl[j * width + i]
            if piece in copysymbols:
                copysymbols.remove(piece)
            elif piece != ".":
                return False

    return True


def filled(pzl):
    return "." not in pzl

def bruteForce(pzl):
    if not invalid(pzl):
        return ""

    if filled(pzl):
        return pzl

    nextEmptyIndex = pzl.index(".")
    symbols = [chr(i + 65) for i in range(len(pzl))]

    for symbol in symbols:
        newpzl = pzl[:nextEmptyIndex] + symbol + pzl[nextEmptyIndex + 1:]
        if invalid(newpzl):
            res = bruteForce(newpzl)
            if res:
                return res

    return ""


if __name__ == "__main__":
    main()

# Charlie Price, pd.3 , 2028