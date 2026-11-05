import sys;args = sys.argv[1:]
HEIGHT=-1
WIDTH=-1
BLOCKS=[]
def main():
    global HEIGHT,WIDTH,BLOCKS
    nox=[]
    
    for arg in args:
        if "x" in arg.lower():
            dimens=arg.lower().split("x")
            nox.append(int(dimens[0]))
            nox.append(int(dimens[1]))
        else:
            nox.append(int(arg))
            
    HEIGHT=nox[0]
    WIDTH=nox[1]
    
    pzl="." * (HEIGHT * WIDTH)
    blocks=[]
    
    for i in range(2,len(nox),2):
        if i + 1 < len(nox):
            blocks.append((nox[i],nox[i+1]))
            
    BLOCKS=blocks
    pzl = bruteForce(pzl,0,[],-999999)

    if pzl:
        pzl=pzl.replace("."," ")
        print("\n".join(pzl[i:i+WIDTH] for i in range(0,len(pzl),WIDTH))+pzl[len(pzl):])
        print(f"Decomposition: {decompose(pzl)}")
        
    else:
        print("No solution")

def bruteForce(pzl,idx,seen,remaining):
    if not seen:
        seen = [False] * len(BLOCKS)
        remaining = HEIGHT * WIDTH - sum(h * w for h, w in BLOCKS)
        if remaining < 0:       
            return ""

    if all(seen):      
        return pzl

    while idx < len(pzl) and pzl[idx] != ".":
        idx += 1
        
    if idx >= len(pzl):
        return ""
    
    r=idx//WIDTH
    c=idx%WIDTH

    for i in possible(seen):
        curh, curw = BLOCKS[i]
        if curh == curw:
            rotations = [(curh, curw)]
        else:
            rotations=[(curh, curw), (curw, curh)]
            
        for h, w in rotations:
            if canput(pzl, r, c, h, w):
                seen[i] = True
                result = bruteForce(put(pzl, r, c, h, w, chr(65 + i)), idx + 1, seen, remaining)
                seen[i] = False
                if result:
                    return result

    if remaining > 0:
        return bruteForce(pzl, idx + 1, seen, remaining - 1)
    return ""


def canput(pzl, r, c, h, w):
    if r + h > HEIGHT or c + w > WIDTH:
        return False
    
    for rh in range(r, r + h):
        for cw in range(c, c + w):
            if pzl[rh * WIDTH + cw] != ".":
                return False
            
    return True

def possible(seen):
    result = []
    passed = set()
    for i, (h, w) in enumerate(BLOCKS):
        if seen[i]:
            continue
        key = (min(h, w), max(h, w))
        if key in seen:
            continue
        passed.add(key)
        result.append(i)
    result.sort(key=area,reverse=True)
    return result

def area(i):
    h, w = BLOCKS[i]
    return h * w

def put(pzl, r, c, h, w, letter):
    lst = list(pzl)
    
    for rh in range(r, r + h):
        for cw in range(c, c + w):
            if rh == r and cw == c:
                lst[rh * WIDTH + cw] = letter.lower() 
            else:
                lst[rh * WIDTH + cw] = letter.upper()
                
    return "".join(lst)

def decompose(pzl):
    seen = [False] * len(pzl)
    decompositions = []

    for idx in range(len(pzl)):
        if seen[idx]:
            continue

        char = pzl[idx]
        
        if char.islower():
            block_index = ord(char) - ord('a')   
            h, w = BLOCKS[block_index]                
            r=idx//WIDTH
            c=idx%WIDTH

            curw = 1
            
            while c + curw < WIDTH and pzl[r*WIDTH + c + curw].upper() == char.upper():
                curw += 1

            curh = 1
            
            while r + curh < HEIGHT and pzl[(r+curh)*WIDTH + c].upper() == char.upper():
                curh += 1
                
            for rh in range(r, r + curh):
                for cw in range(c, c + curw):
                    seen[rh * WIDTH + cw] = True

            decompositions.append(f"{curh}x{curw}")

        elif char == " ":
            r=idx//WIDTH
            c=idx%WIDTH

            curw = 1
            
            while c + curw < WIDTH and pzl[r*WIDTH + c + curw] == " " and not seen[r*WIDTH + c + curw]:
                curw += 1

            curh = 1
            ok = True
            
            while ok and r + curh < HEIGHT:
                for cw in range(c, c + curw):
                    if pzl[(r+curh)*WIDTH + cw] != " " or seen[(r+curh)*WIDTH + cw]:
                        ok = False
                        break
                if ok:
                    curh += 1

            for rh in range(r, r + curh):
                for cw in range(c, c + curw):
                    seen[rh * WIDTH + cw] = True

            decompositions.append(f"{curh}x{curw}")

    return " ".join(decompositions)

if __name__ == "__main__":
    main()

# Charlie Price, pd.3 , 2028