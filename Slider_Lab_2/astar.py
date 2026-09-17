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

def neighbors(puzzle,upos):
  return [neighbor_string(puzzle,upos,nbrpos) for nbrpos in NBRS[upos]] #list comprehension of all possible neighbors given the neighbors switch indeces in the lookup table

def neighbor_string(puzzle, under_index, switch_index):
  #got rid of .join() overhead, saved ~6 seconds
  if under_index<switch_index: 
    return (puzzle[:under_index]+puzzle[switch_index]+puzzle[under_index+1:switch_index]+puzzle[under_index]+puzzle[switch_index+1:],under_index,switch_index) #order to return the neighbor state if underscore comes before the switch element
  return (puzzle[:switch_index]+puzzle[under_index]+puzzle[switch_index+1:under_index]+puzzle[switch_index]+puzzle[under_index+1:],under_index,switch_index) #order to return the neighbor state if the underscore comes after the switch element
  '''lst=[*puzzle]
  lst[under_index],lst[switch_index]=lst[switch_index],lst[under_index]#switches
  return ("".join(lst),under_index,switch_index)#returns tuple, neighbor string, the tiles new index, the tiles old index'''

def aStar(root,goal):
  if not possible(root,goal): #checks inversions, if not possible return a path of "X"
    return (root,"X")
  starting_f=f_distance(root,goal,0) #finds f distance of the start
  starting_h=starting_f # starting f distance is just h because g is 0. (f=g+h) if g=0 because its at the root, then f=0+h, f=h
  openSet = [[] for _ in range(90)] # creates 90 buckets, as 90 is the max f value
  openSet[starting_f].append((starting_f,starting_h,root,"-1",root.index("_"))) #start the openset with all starting values, now we pass initial underscore possition and continue tracking from there
  closedSet={} #closed set of parents as values
  cur_f=starting_f #the current f is just the starting f at the start
  while True:
    lowest_f,lowest_f_h,lowest_f_puzzle,lowest_f_parent,lowest_f_under_index=openSet[cur_f].pop() #gets all tuple values from the current f index, doesnt matter which tuple is popped as they have the same f value
    if lowest_f_puzzle in closedSet: #if the puzzle state has already been discovered
      cur_f=find_best_f(openSet,cur_f) #update current f and continue
      continue
    closedSet[lowest_f_puzzle]=lowest_f_parent # so now we have a parent for the current puzzle, we can add it to the closedSet
    if lowest_f_puzzle==goal: #if we found the goal
      return reconstruct_path(closedSet,lowest_f_puzzle,root) #return the path list, calling the method
    for nbr,new_index,old_index in neighbors(lowest_f_puzzle,lowest_f_under_index):#get the neighbors of the current puzzle
      if nbr not in closedSet: #if we haveent already discovered the neighbor
        newH = lowest_f_h - H_TABLE[nbr[new_index]][old_index] + H_TABLE[nbr[new_index]][new_index] #calculate the new h, which is the previous h value - what the moved tile previously contributed to h + what the moved tile is now contributing to h
        newF = lowest_f-lowest_f_h + 1 + newH #calculate new F, so current f - current H gets current g. if you add one to the g and add the new H, you get the accurate new F value
        openSet[newF].append((newF, newH, nbr, lowest_f_puzzle,old_index))#now in the new fs bucket add the neighbor and its corresponding elements
    cur_f=find_best_f(openSet,cur_f) #find next f

def reconstruct_path(closedSet,lowest_f_puzzle,root):
  path=[goal] #start the path at the goal
  parent=lowest_f_puzzle # the first parent should be "node", the parent of the goal
  while path[-1]!=root: # while the last index of the list is not start
    path.append(parent) #append parents, traversing up the tree
    parent=closedSet[parent] #set the parent to the current nodes parent
  return (root,path[::-1]) #return the tuple of start and path
def find_best_f(openSet,cur_f): #this method just gets the next lowest f value in the openset
  cur_f_loop=True
  cur_f_counter=cur_f
  while cur_f_loop: 
    if openSet[cur_f_counter]!=[]: #finds the next lowest cur_f, so starting at cur_f it increments the index until there is a populated bucket
      cur_f=openSet[cur_f_counter][0][0]
      cur_f_loop=False
    cur_f_counter+=1
  return cur_f #returns the new lowest f

def f_distance(pzl,goal,steps):
  h=h_distance(pzl,goal)
  return steps+h
def h_distance(pzl,goal):
  h_counter=0
  for i,char in enumerate(pzl): #for every character in puzzle
    if char=="_": #skips the underscore
      continue
    h_counter+=H_TABLE[char][i] #gets the initial displacement of all tiles
  return h_counter

def build_h_table(goal):
  h_table = {}
  for char in goal: #for every character in the goal state
      if char == "_": #no need for the underscore h value
          continue
      h_table[char] = {}
      for i in range(len(goal)): # for every characters unique index in the length
          h_table[char][i] = abs(GOAL_POS_CHARS[char][0]-i//WIDTH) +abs(GOAL_POS_CHARS[char][1]-i%WIDTH)  #gets the distance between the goal position of the tile and tile at a certain index in the puzzle, precomupetes every h needed
  return h_table

def build_nbrs():
  dctNbrs={}
  for i in range(WIDTH*HEIGHT):
    dctNbrs[i]=[]
    if i-1>=0 and (i-1)//HEIGHT==i//HEIGHT: #checks if the move left is legal,  it must stay within grid and not change height
      dctNbrs[i].append(i-1)
    if i+1<(length:=WIDTH*HEIGHT) and (i+1)//HEIGHT==i//HEIGHT: # checks if right move is legal, it must stay within grid and not change height
      dctNbrs[i].append(i+1)
    if i+WIDTH<length: # if the move down is within grid
      dctNbrs[i].append(i+WIDTH)
    if i-WIDTH>=0: # if move up is within grid
      dctNbrs[i].append(i-WIDTH)
  return dctNbrs #returns the lookup table

def DRUL(vals): #prints results
    start,path=vals
    moves=[]
    if path!="X": #makes sure the path is solvable
      if [start]!=path:#makes sure the path is more than length 1
        for i,step in enumerate(path[:-1]): #tracks every move up until the last move, the last move is just goal so we dont need to track a move after the goal
            under_index=path[i+1].index("_") #gets index of the underscore in the next move
            prev_under_index=path[i].index("_")#gets current underscore index
            difference=under_index-prev_under_index #gets difference
            move=DCTMOVES[difference]#uses the handy dandy LOOK-UP table!
            moves.append(move)#appends to the moves list

        string_moves="".join(moves) # prints the moves
        print(f"{start}: {string_moves}")
        return
      print(f"{start}: G")#length one so G
      return

    print(f"{start}: {path}") #impossible so x

GOAL=pzls[0]
WIDTH,HEIGHT=dimensions(len(GOAL)) # get the dimension of the grid using a custom helper method
DCTMOVES={-1:"L", 1:"R",-WIDTH:"U",WIDTH:"D",0:""} # lookup table of difference between tiles that corresponds to a move, in DRUL notation
GOAL_POS_CHARS = {char: (i // WIDTH, i % WIDTH) for i, char in enumerate(GOAL)} # lookup table of the row and column values for every character in goal state
H_TABLE=build_h_table(GOAL) #lookup table that stores the precomputted manhattan distance that a specific tile would contribte to h if it was in that position
NBRS=build_nbrs() #lookup table of a tiles index, returns a list of all indeces of possible neighbors

if __name__=="__main__":
    goal=pzls[0]
    for pzl in pzls:
        DRUL(aStar(pzl,goal))

# Charlie Price, 4, 2028