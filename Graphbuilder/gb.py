import sys; args=sys.argv[1:]
import re
DCTDIRECTION={"":".","U":"N","D":"S","L":"W","R":"E","UD":"|","LR":"-","UR":"L","UL":"J","RD":"r","LD":"7","ULD":"<","URD":">","ULR":"^","LRD":"v","ULRD":"+"}
def main():
    graph=grfParse(args)
    edgesStr=grfStrEdges(graph)
    propsStr=grfStrProps(graph)
    if (width:=graph.get("width",0))>0:
        print("\n".join(edgesStr[i:i+width] for i in range(0,graph["size"],width))+edgesStr[graph["size"]:])
    #if jumpsStr:=edgesStr[graph["size"]:]:
     # print(jumpsStr)
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
    reward = "12" # sets default parameters
    pattern = r"G([GN])?(\d*)W?(\d*)R?(\d*)" #gets all data from the setup, type of graph, size, width, and default reward
    size = 0
    width = 0
    graph_type="G"

    if (m:=re.search(pattern, args[0])): #if the pattern is found as an argument
        if m.group(1):
            graph_type=m.group(1) #graph type is first paren group
        if m.group(2): #size is second paren
             size = int(m.group(2) )
        if graph_type=="G" and m.group(3): #if it is a defined gridworld and defined width, set it
            width = int(m.group(3))
        elif graph_type=="G": #if it is a gridworld but no defined width, calculate the width using the dimensions function i wrote for the eights lab
            width=dimensions(size)[0]
        if m.group(4):#default reward
            reward=m.group(4)

    grf = {"rwd": reward, "width": width,"gtype":graph_type} 
    grf["size"]=size #adds parameters to dict

    grf["nativeedges"]=nativeEdges(grf["size"],grf.get("width",0)) #gets a nativeedges list and stores it
    grf["native"] = set((v, nbr) for v, nbrs in grf["nativeedges"].items() for nbr in nbrs) #simple list comprehension that makes all nativeedges into a set of (vertex,neighbor) tuples
    grf["edges"] = set(grf["native"])#dynamic edges set that changes with every action
    grf["vprops"]={} #vproperties dictionary, intiially empty because we havenet done any actions yet.
    grf["eprops"]={} #edge properties

    for arg in args[1:]: #if directives given
        if (ma:=re.search(r"^V([-\d:,#]*[\d:#])?([BRT\d-]*)$",arg)): #this captures all data necessary for a vertex directive
            slices=ma.group(1) #the given slice is the data after the V and before any action, such as a B
            actions="" 
            if ma.group(2): 
                actions=ma.group(2) #actions is the second paren group
                if (rm:=re.search(r"(.*)R(-?\d*)",ma.group(2))):# this handles reward

                    defaultorchange=rm.group(1) #a - before the R means set do default rwd
                    rval=rm.group(2) #this is the value after the R

                    W=set(parseVSlices(slices or "",size,width)) #W set
                    
                    if defaultorchange.endswith("-"): #need to remove any reward for that vertex
                        for v in W:
                            if v in grf["vprops"]: #if the vertex has had a changed default reward, it will be in dictionary, so we need to pop the key.
                                grf["vprops"][v].pop("rwd")
                            #vertex not in vprops will still have default R
                    else: #we now need to change the r value
                        for v in W:
                            if rval: #if the value is defined
                                if v in grf["vprops"]: #if v already in vprops
                                    grf["vprops"][v]["rwd"]=rval #change the value
                                else:
                                    grf["vprops"][v]={"rwd":rval}#add a dictionary to the vertex and assign
                                # this whole block would be much shorter if the defaultorchange function was supported by the grader
                            else: #change value to default
                                if v in grf["vprops"]:
                                    grf["vprops"][v]["rwd"]=grf["rwd"]
                                else:
                                    grf["vprops"][v]={"rwd":grf["rwd"]}


            if "B" in actions: #barrier
                W=set(parseVSlices(slices or "",size,width))#get the set W

                removeme=set() #make a set of vertices to remove
                for a,b in grf["edges"]: 
                    if (a in W) != (b in W): #if the ends differ, the barrier gets cut so you add to the remove set
                        removeme.add((a,b))

                addme=set()
                for a,b in grf["native"]:
                    if (a in W) != (b in W) and (a,b) not in grf["edges"]: #if the ends differ and the tuple is a native edge but not currently an active edge add to add set
                        addme.add((a,b))
                
                grf["edges"]=grf["edges"].difference(removeme).union(addme)

                for edge in removeme: #remove edge properties for removed edges
                    grf["eprops"].pop(edge, None)
        #                     1        2                3         4     5                6
        if (m:=re.search(r"^E([!+*~@])?([-\d:,#]*[\d:#])([NSEW]+)?([=~])([-\d:,#]*[\d:#])?([RT\d-]*)$",arg)): 
            slice1regex=m.group(2)
            if s2r:=m.group(5): #if second slice exists
                slice2regex=m.group(5)
            direction=m.group(4)
            if c:=m.group(3):# if cardinal direction group exists
                cardinal=c
            management=""
            defaultorchange=""
            rval=""
            if (r:=m.group(6)): #if there is an R
                if (rm:=re.search(r"(.*)R(-?\d*)",m.group(6))):    #parse R
                    defaultorchange=rm.group(1) #a - before the R means set do default rwd
                    rval=grf["rwd"]
                    if rv:=rm.group(2): #this is the value after the R
                        rval=rv
            if (mngmt:=m.group(1)): #if there is a management group
                management=mngmt
            
            #print(f"management:{management} slice1: {slice1regex} direction: {direction} slice2: {slice2regex} defaultorchange: {defaultorchange} val:{rval}")
            slice1=parseVSlices(slice1regex,size,width) #always a first slice
            edgeslices=set()
            if s2r: #if second slice
                slice2=parseVSlices(slice2regex,size,width)
                edgeslices=set(zip(slice1,slice2)) #zip up the two slices and make a set of tuples,avoiding duplicates

            else: #if there is no second slice, there must be a cardinal direction
                if "N" in cardinal:# north, index - width
                    for a in slice1: 
                        if (a,a-width) in grf["native"]: #checks if move exists in native
                            edgeslices.add((a,a-width))
                if "E" in cardinal: #east, index +1 
                    for a in slice1:
                        if (a,a+1) in grf["native"]: 
                            edgeslices.add((a,a+1))
                if "W" in cardinal: #west, index -1
                    for a in slice1:
                        if (a,a-1) in grf["native"]:
                            edgeslices.add((a,a-1))
                if "S" in cardinal: #south, index + width
                    for a in slice1:
                        if (a,a+width) in grf["native"]:
                            edgeslices.add((a,a+width))

            if direction=="=": #swap vertices in edges, ie bidirection
                edgeslices=set(edgeslices.union(set([(b,a) for a,b in edgeslices])))
            if "!"==management: #remove existing edges
                for a,b in edgeslices:
                    if (a,b) in grf["edges"]:
                        grf["edges"].discard((a,b))
                        grf["eprops"].pop((a,b),None)

            if "+"==management: # add if not existing with properties, ignore existing edges
                for a,b in edgeslices:
                    if (a,b) not in grf["edges"]:
                        grf["edges"].add((a,b))
                        if rval: #if the value is defined
                            if (a,b) in grf["eprops"]: #if v already in vprops
                                grf["eprops"][(a,b)]["rwd"]=rval #change the value
                            else:
                                grf["eprops"][(a,b)]={"rwd":rval}#add a dictionary to the vertex and assign

                            # this whole block would be much shorter if the defaultorchange function was supported by the grader
            
            if "*" == management: # add if missing, apply properties regardless
                for a,b in edgeslices:
                    if (a,b) not in grf["edges"]:
                        grf["edges"].add((a,b))
                    if rval: #if the value is defined
                        if (a,b) in grf["eprops"]: #if v already in vprops
                            grf["eprops"][(a,b)]["rwd"]=rval #change the value
                        else:
                            grf["eprops"][(a,b)]={"rwd":rval}#add a dictionary to the vertex and assign
                        # this whole block would be much shorter if the defaultorchange function was supported by the grader
            
            if ""==management or "~" ==management: #default toggles edges
                for a,b in edgeslices:
                    if (a,b) not in grf["edges"]:
                        grf["edges"].add((a,b))
                        if rval: #if the value is defined
                            if (a,b) in grf["eprops"]: #if v already in vprops
                                grf["eprops"][(a,b)]["rwd"]=rval #change the value
                            else:
                                grf["eprops"][(a,b)]={"rwd":rval}#add a dictionary to the vertex and assign
                    else:
                        grf["edges"].remove((a, b)) #remove edge
                        if (a,b) in grf["eprops"]: #if the vertex has had a changed default reward, it will be in dictionary, so we need to pop the key.
                            grf["eprops"].pop((a, b)) #remove key
            
            if "@"==management: #apply properties to existing edges, disregard new edges
                for a,b in edgeslices:
                    if (a,b) in grf["edges"]:
                        if rval: #if the value is defined
                            if (a,b) in grf["eprops"]: #if v already in vprops
                                grf["eprops"][(a,b)]["rwd"]=rval #change the value
                            else:
                                grf["eprops"][(a,b)]={"rwd":rval}#add a dictionary to the vertex and assign
                            # this whole block would be much shorter if the defaultorchange function was supported by the grader
            


    nbrs = {v: [] for v in range(size)}
    for a, b in grf["edges"]:
        nbrs[a].append(b)
    for v in nbrs:
        nbrs[v].sort() #sorts the vertices
    grf["nbrs"] = nbrs #adds new key to be the final edge setup

    return grf

def parseVSlices(strSlices,size,width):
    vs=[*range(size)] #basic 0-size list
    lst=[]
    for cur in strSlices.split(","):
        if (m:=re.search(r"(\d*)#(\d*)", cur)): #rectangle slice
            if width>0:
                tl=0
                if m.group(1):
                    tl = int(m.group(1)) 
                br=size-1
                if m.group(2):
                    br = int(m.group(2))
                rowtl = tl // width #row and column for top left and top right of the rectangle
                coltl = tl % width
                rowbr = br // width
                colbr = br % width
                for row in range(min(rowtl, rowbr), max(rowtl, rowbr) + 1): #iterate throught he corners
                    for col in range(min(coltl, colbr), max(coltl, colbr) + 1):
                        if row * width + col < size:
                            lst.append(row * width + col) #append index of all 4 corners

        elif(m:=re.search(r"(-?\d*):(-?\d*):?(-?\d*)",cur)): #normal slice
            start=None
            stop=None
            step=None
            if (sta:=m.group(1)):
                start=int(sta)  
            if(sto:=m.group(2)):
                stop=int(sto)
            if (ste:=m.group(3)):
                step=int(ste)
            lst+=[*vs[start:stop:step]] #gets data and returns the slice

        elif(m:=re.search(r"(-?\d*)",cur)): #single vertex 
            if (v:=m.group(1)):
                lst+=[vs[int(v)]] 
   
    return lst

def grfStrJumps(grf):
    jumps = sorted(grf["edges"] - grf["native"]) #jumps are edges that do not exist as native edges, so the jumps are the result of subtracting the two sets

    if not jumps:
        return ""
    
    startingb="" #setting up starting and ending vertices for directional and bidirectional edges
    startingd=""
    endingb=""
    endingd=""

    bidirectionalseen=[] #tracks bidirectional pairs, so when (5,8) is bidirectional it only prints 5=8 not 5,8=8,5

    for a,b in jumps:
        if a==b or (b,a) not in jumps: #if the vertices are equal or the vertices do not have the opposite alignment of indeces in jumps, they are directional
            startingd+=f"{a},"
            endingd+=f"{b},"

        elif (a,b) not in bidirectionalseen and (b,a) not in bidirectionalseen: #else, the jump is bidirectional, the vertices have both alignments of indeces
            startingb+=f"{a},"
            endingb+=f"{b},"
            bidirectionalseen.append((a,b))

    startingb=startingb[:-1] #shave of the last comma
    startingd=startingd[:-1]
    endingb=endingb[:-1]
    endingd=endingd[:-1]

    jumpsstr="" #string of jumps
    #next two if statements build the string if the jumps exist
    if startingd and endingd: 
        jumpsstr+=f"\nJumps: {startingd}~{endingd}"
        if startingb and endingb:
            jumpsstr+=f";{startingb}={endingb}"

    elif startingb and endingb:
        jumpsstr+=f"\nJumps: {startingb}={endingb}"
        if startingd and endingd:
            jumpsstr+=f";{startingd}~{endingd}"

    return jumpsstr

def grfSize(grf):
    return grf["size"]

def gridFromEdges(grf,edges,width):
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
        grid+=DCTDIRECTION[cur] #just uses the global lookup table given all direction is DRUL format
    return grid
    

def grfStrEdges(grf):
    grid=""
    if grf.get("width",0)>0:
       #grid="\n".join(gridFromEdges(grf,grf["nbrs"],grf.get("width",0))[i:i+grf["width"]] for i in range(0,grf["size"],grf["width"])) #makes graph a grid if gridworld graph
       grid+= gridFromEdges(grf, grf["nbrs"], grf["width"]) #get grid
    
    if jumpsstr:=grfStrJumps(grf): #if there are jumps call function and add them to string
        grid+=jumpsstr
    return grid

def nativeEdges(size,width):
    nativeedges={i:[] for i in range(size)}
    if width<=0:
        return nativeedges
    for i in range(size):
        col=i%width #column
        if i-width>=0: #move up is within bounds
            nativeedges[i].append(i-width)
        if col>0: #column not on left edge
             nativeedges[i].append(i-1)
        if i+1<size and col<width-1: #column not on right edge
            nativeedges[i].append(i+1)
        if  i+width<size: #move down is within bounds
            nativeedges[i].append(i+width)
    return nativeedges

def grfEProps(grf,vtxIdx1,vtxIdx2):
    return grf["eprops"].get((vtxIdx1,vtxIdx2),{})

def grfNbrs(grf,vtxIdx):
    return grf["nbrs"][vtxIdx]

def grfGProps(grf):
    #print(grf)
    dct={"rwd":grf["rwd"]}
    if grf["gtype"]!="N":
        dct["width"]=grf["width"]
    return dct  

def grfStrProps(grf):
    return ", ".join(f"{key}: {value}" for key, value in grfGProps(grf).items())+"\n"+"\n".join([f"{v}: " + "rwd: " +f"{grf['vprops'][v]['rwd']}" for v in sorted(grf["vprops"])])+"\n"+"\n".join([f"{(a,b)}: rwd: {grf['eprops'][(a,b)]['rwd']}" for a,b in sorted(grf["eprops"])])

def grfVProps(grf,vtxIdx):
    return grf["vprops"].get(vtxIdx,{})

if __name__=="__main__":
    main()

#Charlie Price, pd 3, 2028