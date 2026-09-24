import sys; args=sys.argv[1:]
import time

def dimensions(num:int):
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

def neighbors(puzzle): #returns a list of the neighbors of the puzzle
 
 neighbor_list=[]
 under_index=puzzle.index("_")
 if under_index-1>=0 and (under_index-1)//height==under_index//height: #checks if the move left is legal,  it must stay within grid and not change height
  neighbor_list.append(neighbor_string(puzzle,under_index,under_index-1)) #calls helper method, then adds the neighbor state to list
 
 if under_index+1<length and (under_index+1)//height==under_index//height: # checks if right move is legal, it must stay within grid and not change height
  neighbor_list.append(neighbor_string(puzzle,under_index,under_index+1))
 
 if under_index+width<length: # if the move down is within grid
  neighbor_list.append(neighbor_string(puzzle,under_index,under_index+width))
 
 if under_index-width>=0: # if move up is within grid
   neighbor_list.append(neighbor_string(puzzle,under_index,under_index-width))
   
 return neighbor_list

def neighbor_string(puzzle, under_index, switch_index):
 
 if under_index<switch_index: 
  return puzzle[:under_index]+puzzle[switch_index]+puzzle[under_index+1:switch_index]+puzzle[under_index]+puzzle[switch_index+1:] #order to return the neighbor state if underscore comes before the switch element
 return puzzle[:switch_index]+puzzle[under_index]+puzzle[switch_index+1:under_index]+puzzle[switch_index]+puzzle[under_index+1:] #order to return the neighbor state if the underscore comes after the switch element
  
def BFS(start): #bfs algorithm method
 level=0
 parseMe=[(start,level)] #initialize the nodes to get the neighbors of
 dctSeen={start:""} #dictionary of nodes that have been passed, the value is the parent
 dct_nodes={start:(0,len(neighbors(start)),len(neighbors(start)))} #level,num neighbors,num children
 while parseMe: #while parseMe is not empty
  node,cur_level = parseMe.pop(0) # removes the first index of parseMe and stores it in node
  num_not_parents=0
  for nbr in [n for n in neighbors(node) if n not in dctSeen]: #simple list comprehensions of neighbors not in dictionary of seen nodes
   num_not_parents+=1
   parseMe.append((nbr,cur_level+1)) #if the current neighbor isnt the goal, we need to add it to the list of nodes we need to process
   dctSeen[nbr]=node #because we only loop through nodes not in dictionary, we can add the neighbor as a key and the value as its parent
  if node not in dct_nodes:
    dct_nodes[node]=(cur_level,len(neighbors(node)),num_not_parents)

 return dct_nodes #this will only be reached if no goal is found, defaulting to the required start position, the time it took, and steps of -1 as a tuple

start = args[0] # start is first argument after the python file name
length=len(start)

width,height=dimensions(length) # get the dimension of the grid using a custom helper method
time_start=time.time()

def print_levels(dct_nodes):
  dct_parent_kids={"40":0,"30":0,"20":0,"31":0,"21":0,"11":0,"22":0,"12":0,"02":0,"13":0,"03":0,"04":0}
  for keys in dct_nodes:
    max_nums=dct_nodes[keys][1]
    children=dct_nodes[keys][2]
    parents=max_nums-children
    cur_num=dct_parent_kids[f"{parents}{children}"]
    dct_parent_kids[f"{parents}{children}"]=cur_num+1
  for keys,val in dct_parent_kids.items():
    print(f"{keys}: {val}")

if __name__=="__main__": # executes code below
  print_levels(BFS(start)) # prints the BFS result of the inputs

# Charlie Price, 4, 2028