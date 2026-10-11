import sys; args=sys.argv[1:]
import re


def dimensions(num):
 divisor = 1 #tracks the divisor
 factors=[] #list of factors

 while divisor <=num: # factors of a number must be less than or equal to the number, hence the while loop check
  quotient = num/divisor #gets the quotient of number and divisor
  if int(quotient)+.0==quotient: # checks if the quotient has decimal values of .0
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
    pattern = r"G[GN]?(\d*)W?(\d*)R?(\d*)"
    size = 0
    width = -1

    if (m:=re.search(pattern, args[0], re.I)):
        if m.group(1):
             size = int(m.group(1) )
        if m.group(2):
            width = int(m.group(2))
        else:
            width=dimensions(size)[0]
        if m.group(3):
            reward=m.group(3)

    grf = {"rwd": reward, "width": width}
    props = grfGProps(grf)
    props["size"]=size
    return props
def grfSize(grf):
    print(grf["size"])
    return grf["size"]

def grfGProps(grf):
    #print(grf)
    return {"rwd":grf["rwd"],"width":grf["width"]}

def grfStrProps(grf):
    return f"rwd: {grf['rwd']}, width: {grf['width']}"

def grfVProps(grd,vtxIdx):
    return {}

if __name__=="__main__":
    grfParse(args)

#Charlie Price, pd 3, 2028