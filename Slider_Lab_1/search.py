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
  
def BFS(start,goal): #bfs algorithm method

 if start == goal: #if the start is the same as the goal, return the start, time, and 0 steps
  time_end=time.time()-time_start
  steps=0
  if time_end<0.001: #make sure 3 sig figs
    time_end=0.000
  return ([start],f"{time_end:#.3g}s",steps)
 
 parseMe=[start] #initialize the nodes to get the neighbors of
 dctSeen={start:""} #dictionary of nodes that have been passed, the value is the parent
 
 while parseMe: #while parseMe is not empty
  node = parseMe.pop(0) # removes the first index of parseMe and stores it in node
  
  for nbr in [n for n in neighbors(node) if n not in dctSeen]: #simple list comprehensions of neighbors not in dictionary of seen nodes
   if nbr == goal: #if a neighbor equals goal
    path=[goal] #start the path at the goal
    parent=node # the first parent should be "node", the parent of the goal
    
    while path[-1]!=start: # while the last index of the list is not start
     path.append(parent) #append parents, traversing up the tree
     parent=dctSeen[parent] #set the parent to the current nodes parent
    
    time_end=time.time()-time_start#return difference of time
    if time_end<0.001: #make sure 3 sig figs
      time_end=0.000
    return (path[::-1],f"{time_end:#.3g}s",len(path)-1)# because we appended parents sequentially, we need to reverse to list to have the start node as index 0, we then return this as a tuple with index 0 being the list, index 1 being the time it took formatted to 3 significant digits, and index 2 being the amount of steps
    steps
   parseMe.append(nbr) #if the current neighbor isnt the goal, we need to add it to the list of nodes we need to process
   dctSeen[nbr]=node #because we only loop through nodes not in dictionary, we can add the neighbor as a key and the value as its parent
   
 time_end=time.time()-time_start
 if time_end<0.001: #make sure 3 sig figs
  time_end=0.000
 return ([start],f"{time_end:#.3g}s",-1) #this will only be reached if no goal is found, defaulting to the required start position, the time it took, and steps of -1 as a tuple
  
def print_bands(vals): #prints results
 path,time,path_length=vals # BFS function returns tuple: (path,time,path_length)
 k=5 #i chose a k of 5
 lines=(path_length+1)//k # this gets the number of times it needs to print steps in lines of 5
 
 while lines>=1: #while it still needs to print 5 
  
  for _ in range(height): #throw away variable, only need to use it for the repetition of code
   line_str="" #string that represent a line
   for i in range(k): #loops over k, i chose 5
    for w in range(width): #loops over width
     
     line_str+=path[i][w] #adds the corresponding step element 
     if w==width-1: #if the last i width element, print double space to indicate another puzzle step
      line_str+="  "
      
    path[i]=path[i][width:] #clever trick remove elements already printed so the next lines prints the next level
   print(line_str)#prints the line
  print("")
   
  lines-=1 #subtracts the current line level
  path=path[k:] #removes the steps printed
  
 for _ in range(height): 
  
  line_str=""
  for i in range(len(path)):#now we get to the last lines, able to print # of steps <5
   for w in range(width):
    
    line_str+=path[i][w]
    if w==width-1:
     line_str+="  "
     
   path[i]=path[i][width:] 
  print(line_str)
 print("")
 print(f"Steps: {path_length}\n") #prints path length
 print("Time: "+time) #print time

start = args[0] # start is first argument after the python file name
under_index=start.index("_") #gets underscore index in the start state

#array of elements in start without underscore
no_underscore=[char for char in start[:under_index]+start[under_index+1:]]
no_underscore.sort() #sort that array

#default to an empty goal state
goal="".join(no_underscore)+"_"# converts sorted non-underscore elements to a string and adds the underscore at the end

if args[1:]: # if there is a goal argument, assing goal to that value
 goal=args[1]
(length:=len(start))

width,height=dimensions(length) # get the dimension of the grid using a custom helper method
time_start=time.time()

if __name__=="__main__": # executes code below
 print_bands(BFS(start,goal)) # prints the BFS result of the inputs

# Charlie Price, 4, 2028