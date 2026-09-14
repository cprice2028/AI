import sys; args=sys.argv[1:]
pzls=open(args[0]).read().splitlines()
def possible(start,goal): #return true if same parity, false if different
  start_no_underscore=start[:start.index("_")]+start[start.index("_")+1:] #gets a string for both the start and goal without the underscore
  goal_no_underscore=goal[:goal.index("_")]+goal[goal.index("_")+1:]
  row_from_bottom_start=HEIGHT- (start.index("_")//WIDTH)
  row_from_bottom_goal=HEIGHT - (goal.index("_")//WIDTH)
  inversions_start=0 #sets up counters for each states inversions
  inversions_goal=0
  for i,element in enumerate(goal_no_underscore): #simple nested loop that counts how many elements to the right of a certain element are less than, inversion
    for element_slice in goal_no_underscore[i:]:
      if element<element_slice:
        inversions_goal+=1

  for i,element in enumerate(start_no_underscore):#simple nested loop that counts how many elements to the right of a certain element are less than, inversion
    for element_slice in start_no_underscore[i:]:
      if element<element_slice:
        inversions_start+=1
  return (inversions_goal+row_from_bottom_goal)%2==(inversions_start+row_from_bottom_start)%2

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
 if under_index-1>=0 and (under_index-1)//HEIGHT==under_index//HEIGHT: #checks if the move left is legal,  it must stay within grid and not change height
  neighbor_list.append(neighbor_string(puzzle,under_index,under_index-1)) #calls helper method, then adds the neighbor state to list
 
 if under_index+1<(length:=len(puzzle)) and (under_index+1)//HEIGHT==under_index//HEIGHT: # checks if right move is legal, it must stay within grid and not change height
  neighbor_list.append(neighbor_string(puzzle,under_index,under_index+1))
 
 if under_index+WIDTH<length: # if the move down is within grid
  neighbor_list.append(neighbor_string(puzzle,under_index,under_index+WIDTH))
 
 if under_index-WIDTH>=0: # if move up is within grid
   neighbor_list.append(neighbor_string(puzzle,under_index,under_index-WIDTH))
   
 return neighbor_list

def neighbor_string(puzzle, under_index, switch_index):
  lst=[*puzzle]
  lst[under_index],lst[switch_index]=lst[switch_index],lst[under_index]
  return "".join(lst)
'''def BFS(start,goal): #bfs algorithm method

 if start == goal: #if the start is the same as the goal, return the start, time, and 0 steps
  return ([start],[start])
 
 parseMe=[start] #initialize the nodes to get the neighbors of
 dctSeen={start:""} #dictionary of nodes that have been passed, the value is the parent
 
 for node in parseMe: #while parseMe is not empty # removes the first index of parseMe and stores it in node
 #while parseMe:
  #node = parseMe.pop(0)
  for nbr in [n for n in neighbors(node) if n not in dctSeen]: #simple list comprehensions of neighbors not in dictionary of seen nodes
   if nbr == goal: #if a neighbor equals goal
    path=[goal] #start the path at the goal
    parent=node # the first parent should be "node", the parent of the goal
    
    while path[-1]!=start: # while the last index of the list is not start
     path.append(parent) #append parents, traversing up the tree
     parent=dctSeen[parent] #set the parent to the current nodes parent
    
    
    return ([start],path[::-1])# because we appended parents sequentially, we need to reverse to list to have the start node as index 0, we then return this as a tuple with index 0 being the list, index 1 being the time it took formatted to 3 significant digits, and index 2 being the amount of steps
   parseMe.append(nbr) #if the current neighbor isnt the goal, we need to add it to the list of nodes we need to process
   dctSeen[nbr]=node #because we only loop through nodes not in dictionary, we can add the neighbor as a key and the value as its parent
   
 return ([start],[start]) #this will only be reached if no goal is found, defaulting to the required start position, the time it took, and steps of -1 as a tuple
'''
def aStar(root,goal):
  if not possible(root,goal):
    return (root,"X")
  starting_f=f_distance(root,goal,0)
  starting_h=h_distance(root,goal)
  openSet=[(starting_f,starting_h,root,"-1")]
  closedSet={}
  while True:
    openSet.sort()
    lowest_f_tuple=openSet.pop(0)
    lowest_f,lowest_f_h,lowest_f_puzzle,lowest_f_parent=lowest_f_tuple
    if lowest_f_puzzle in closedSet:
      continue
    closedSet[lowest_f_puzzle]=lowest_f_parent
    if lowest_f_puzzle==goal:
      path=[goal] #start the path at the goal
      parent=lowest_f_puzzle # the first parent should be "node", the parent of the goal
      
      while path[-1]!=root: # while the last index of the list is not start
        path.append(parent) #append parents, traversing up the tree
        parent=closedSet[parent] #set the parent to the current nodes parent
      return (root,path[::-1])
    for nbr in neighbors(lowest_f_puzzle):
      newF = lowest_f-lowest_f_h +1 + (newH:=h_distance(nbr,goal))
      if nbr not in closedSet:
        openSet.append((newF, newH, nbr, lowest_f_puzzle))

    
def f_distance(pzl,goal,steps):
  h=h_distance(pzl[:pzl.index("_")]+pzl[pzl.index("_")+1:],goal[:goal.index("_")]+goal[goal.index("_")+1:])
  return steps+h
def h_distance(pzl,goal):
  h_counter=0
  for i in range(len(pzl)):
    i_val=pzl[i]
    goal_i=goal.index(i_val)
    row_i,col_i=(i//WIDTH,i%WIDTH)
    row_goal,col_goal=(goal_i//WIDTH,goal_i%WIDTH)
    h_counter+=abs(row_goal-row_i)+abs(col_goal-col_i)
  return h_counter
    
def DRUL(vals): #prints results
    start,path=vals
    moves=[]
    if path!="X":
      if [start]!=path:
        for i,step in enumerate(path[:-1]):
            under_index=path[i+1].index("_")
            prev_under_index=path[i].index("_")
            difference=under_index-prev_under_index
            move=DCTMOVES[difference]
            moves.append(move)

        string_moves="".join(moves)            
        print(f"{start}: {string_moves}")
        return
      print(f"{start}: G")
      return

    print(f"{start}: {path}")

GOAL=pzls[0]
WIDTH,HEIGHT=dimensions(len(GOAL)) # get the dimension of the grid using a custom helper method
DCTMOVES={-1:"L", 1:"R",-WIDTH:"U",WIDTH:"D",0:""}

def start_puzzle(pzl,goal):#method that handles one puzzle at a time
  '''if not inversions(pzl,goal): #if different parity, no solution should be found
    DRUL([pzl]) #prints only the start, the time, and the steps associated with no solution
  else:#same parity, solution exists, so call method to find the path to the goal state
    DRUL(BFS(pzl,goal)) # prints the BFS result of the inputs
  '''
  DRUL(aStar(pzl,goal))


if __name__=="__main__":
    goal=pzls[0]
    for pzl in pzls:
        start_puzzle(pzl,goal)



# Charlie Price, 4, 2028