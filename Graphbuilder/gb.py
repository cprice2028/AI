import sys; args=sys.argv[1:]
import re
DCTDIRECTION={"":".","U":"N","D":"S","L":"W","R":"E","UD":"|","LR":"-","UR":"L","UL":"J","RD":"r","LD":"7","ULD":"<","URD":">","ULR":"^","LRD":"v","ULRD":"+"}
def main():
    graph=grfParse(args)
    edgesStr=grfStrEdges(graph)
    propsStr=grfStrProps(graph)
    width = graph.get("width",0)
    if width>0:
        print("\n".join(edgesStr[i:i+width] for i in range(0,graph["size"],width)))
    else:
        print("")
    print(propsStr)

def dimensions(num):
 if num<1:
    return (0,9)
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

def grfParse(args):
    reward = "12"
    pattern = r"G([GN])?(\d*)W?(\d*)R?(\d*)"
    size = 0
    width = 0
    graph_type="G"

    if (m:=re.search(pattern, args[0])):
        if m.group(1):
            graph_type=m.group(1)
        if m.group(2):
             size = int(m.group(2) )
        if graph_type=="G" and m.group(3):
            width = int(m.group(3))
        elif graph_type=="G":
            width=dimensions(size)[0]
        if m.group(4):
            reward=m.group(4)

    grf = {"rwd": reward, "width": width,"gtype":graph_type}
    grf["size"]=size
    grf["nativeedges"]=nativeEdges(grf["size"],grf.get("width",0))
    grf["native"] = set((v, nbr) for v, nbrs in grf["nativeedges"].items() for nbr in nbrs)
    grf["edges"] = set(grf["native"])
    grf["vprops"]={}

    for arg in args[1:]:
        if (ma:=re.search(r"^V([-\d:,#]*[\d:#])?([BRT\d-]*)$",arg)):
            slices=ma.group(1)
            actions=""
            if ma.group(2):
                actions=ma.group(2)
                if (rm:=re.search(r"(.*)R(-?\d*)",ma.group(2))):

                    defaultorchange=rm.group(1)
                    rval=rm.group(2)

                    W=set(parseVSlices(slices or "",size,width))
                    
                    if defaultorchange.endswith("-"):
                        for v in W:
                            if v in grf["vprops"]:
                                grf["vprops"][v].pop("rwd")
                    else:
                        for v in W:
                            if rval:
                                if v in grf["vprops"]:
                                    grf["vprops"][v]["rwd"]=rval
                                else:
                                    grf["vprops"][v]={"rwd":rval}
                            else:
                                if v in grf["vprops"]:
                                    grf["vprops"][v]["rwd"]=grf["rwd"]
                                else:
                                    grf["vprops"][v]={"rwd":grf["rwd"]}


            if "B" in actions:
                W=set(parseVSlices(slices or "",size,width))

                removeme=set({})
                for a,b in grf["edges"]:
                    if (a in W) != (b in W):
                        removeme.add((a,b))

                addme=set({})
                for a,b in grf["native"]:
                    if (a in W) != (b in W) and (a,b) not in grf["edges"]:
                        addme.add((a,b))
                
                grf["edges"]=grf["edges"].difference(removeme).union(addme)

    nbrs = {v: [] for v in range(size)}
    for a, b in grf["edges"]:
        nbrs[a].append(b)
    for v in nbrs:
        nbrs[v].sort()
    grf["nbrs"] = nbrs

    return grf

def parseVSlices(strSlices,size,width):
    vs=[*range(size)]
    lst=[]
    for cur in strSlices.split(","):
        if (m:=re.search(r"(\d*)#(\d*)", cur)):
            if width>0:
                tl=0
                if m.group(1):
                    tl = int(m.group(1)) 
                br=size-1
                if m.group(2):
                    br = int(m.group(2))
                rowtl = tl // width
                coltl = tl % width
                rowbr = br // width
                colbr = br % width
                for row in range(min(rowtl, rowbr), max(rowtl, rowbr) + 1):
                    for col in range(min(coltl, colbr), max(coltl, colbr) + 1):
                        if row * width + col < size:
                            lst.append(row * width + col)

        elif(m:=re.search(r"(-?\d*):(-?\d*):?(-?\d*)",cur)):
            start=None
            stop=None
            step=None
            if (sta:=m.group(1)):
                start=int(sta)  
            if(sto:=m.group(2)):
                stop=int(sto)
            if (ste:=m.group(3)):
                step=int(ste)
            lst+=[*vs[start:stop:step]]

        elif(m:=re.search(r"(-?\d*)",cur)):
            if (v:=m.group(1)):
                lst+=[vs[int(v)]] 
   
    return lst

def grfSize(grf):
    return grf["size"]

def gridFromEdges(edges,width):
    if width==0:
        return ""
    grid=""
    for v,nbrs in edges.items():
        cur=""
        for nbr in nbrs:
            if v-width==nbr:
                cur+="U"
            if v-1==nbr and v % width != 0:
                cur+="L"
            if v+1==nbr and v % width != width - 1:
                cur+="R"
            if v+width==nbr:
                cur+="D"
        grid+=DCTDIRECTION[cur]
    return grid
    

def grfStrEdges(grf):
    return gridFromEdges(grf["nbrs"],grf.get("width",0))

def nativeEdges(size,width):
    nativeedges={i:[] for i in range(size)}
    if width<=0:
        return nativeedges
    for i in range(size):
        col=i%width
        if i-width>=0:
            nativeedges[i].append(i-width)
        if col>0:
             nativeedges[i].append(i-1)
        if i+1<size and col<width-1:
            nativeedges[i].append(i+1)
        if  i+width<size:
            nativeedges[i].append(i+width)
    return nativeedges

def grfEProps(grf,vtxIdx1,vtxIdx2):
    return {}

def grfNbrs(grf,vtxIdx):
    return grf["nbrs"][vtxIdx]

def grfGProps(grf):
    #print(grf)
    dct={"rwd":grf["rwd"]}
    if grf["gtype"]!="N":
        dct["width"]=grf["width"]
    return dct  

def grfStrProps(grf):
    return ", ".join(f"{key}: {value}" for key, value in grfGProps( grf).items())+"\n"+"\n".join([f"{v}: " + "rwd: " +f"{grf['vprops'][v]['rwd']}" for v in sorted(grf["vprops"])])

def grfVProps(grf,vtxIdx):
    return grf["vprops"].get(vtxIdx,{})

if __name__=="__main__":
    main()

#Charlie Price, pd 3, 2028