import sys
import multiprocessing
import cProfile

# -------------------------------------------------------------------
# Helper Functions (Defined at Top-Level for Pickling)
# -------------------------------------------------------------------

def dimensions(num: int):
    divisor = 1
    factors = []
    while divisor <= num:
        quotient = num / divisor
        if int(quotient) + 0.0 == quotient:
            factors.append((int(quotient), divisor))
        divisor += 1
    smallest_w, current_height = factors[0]
    for w, h in factors:
        if w >= h and w < smallest_w:
            smallest_w = w
            current_height = h
    return (smallest_w, current_height)

def possible(start, goal, width, height):
    start_no_u = start[:start.index("_")] + start[start.index("_") + 1:]
    goal_no_u = goal[:goal.index("_")] + goal[goal.index("_") + 1:]
    row_from_bottom_start = height - (start.index("_") // width)
    row_from_bottom_goal = height - (goal.index("_") // width)
    
    inversions_start = sum(1 for i, el in enumerate(start_no_u) for slice_el in start_no_u[i:] if el < slice_el)
    inversions_goal = sum(1 for i, el in enumerate(goal_no_u) for slice_el in goal_no_u[i:] if el < slice_el)
    
    return (inversions_goal + row_from_bottom_goal) % 2 == (inversions_start + row_from_bottom_start) % 2

def neighbor_string(puzzle, under_index, switch_index):
    if under_index < switch_index: 
        return (puzzle[:under_index] + puzzle[switch_index] + puzzle[under_index + 1:switch_index] + puzzle[under_index] + puzzle[switch_index + 1:], under_index, switch_index)
    return (puzzle[:switch_index] + puzzle[under_index] + puzzle[switch_index + 1:under_index] + puzzle[switch_index] + puzzle[under_index + 1:], under_index, switch_index)

def neighbors(puzzle, upos, nbrs_table):
    return [neighbor_string(puzzle, upos, nbrpos) for nbrpos in nbrs_table[upos]]

def find_best_f(openSet, cur_f):
    cur_f_counter = cur_f
    while True: 
        if openSet[cur_f_counter] != []:
            return openSet[cur_f_counter][0][0]
        cur_f_counter += 1

def f_distance(pzl, goal, steps, h_table):
    return steps + h_distance(pzl, goal, h_table)

def h_distance(pzl, goal, h_table):
    h_counter = 0
    for i, char in enumerate(pzl):
        if char == "_":
            continue
        h_counter += h_table[char][i]
    return h_counter

def reconstruct_path(closedSet, lowest_f_puzzle, root, goal):
    path = [goal]
    parent = lowest_f_puzzle
    while path[-1] != root:
        path.append(parent)
        parent = closedSet[parent]
    return (root, path[::-1])

def aStar(root, goal, width, height, h_table, nbrs_table):
    if not possible(root, goal, width, height):
        return (root, "X")
    starting_f = f_distance(root, goal, 0, h_table)
    starting_h = starting_f
    openSet = [[] for _ in range(90)]
    openSet[starting_f].append((starting_f, starting_h, root, "-1", root.index("_")))
    closedSet = {}
    cur_f = starting_f
    
    while True:
        lowest_f, lowest_f_h, lowest_f_puzzle, lowest_f_parent, lowest_f_under_index = openSet[cur_f].pop()
        if lowest_f_puzzle in closedSet:
            cur_f = find_best_f(openSet, cur_f)
            continue
        closedSet[lowest_f_puzzle] = lowest_f_parent
        
        if lowest_f_puzzle == goal:
            return reconstruct_path(closedSet, lowest_f_puzzle, root, goal)
            
        for nbr, new_index, old_index in neighbors(lowest_f_puzzle, lowest_f_under_index, nbrs_table):
            if nbr not in closedSet:
                newH = lowest_f_h - h_table[nbr[new_index]][old_index] + h_table[nbr[new_index]][new_index]
                newF = lowest_f - lowest_f_h + 1 + newH
                openSet[newF].append((newF, newH, nbr, lowest_f_puzzle, old_index))
        cur_f = find_best_f(openSet, cur_f)

def DRUL(vals, dct_moves):
    start, path = vals
    moves = []
    if path != "X":
        if [start] != path:
            for i, step in enumerate(path[:-1]):
                under_index = path[i + 1].index("_")
                prev_under_index = path[i].index("_")
                difference = under_index - prev_under_index
                moves.append(dct_moves[difference])
            return f"{start}: {''.join(moves)}"
        return f"{start}: G"
    return f"{start}: {path}"

def solve_and_drul(pzl, goal, width, height, h_table, nbrs_table, dct_moves):
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = DRUL(aStar(pzl, goal, width, height, h_table, nbrs_table), dct_moves)
    
    profiler.disable()
    return result

def build_h_table(goal, width, goal_pos_chars):
    h_table = {}
    for char in goal:
        if char == "_":
            continue
        h_table[char] = {}
        for i in range(len(goal)):
            h_table[char][i] = abs(goal_pos_chars[char][0] - i // width) + abs(goal_pos_chars[char][1] - i % width)
    return h_table

def build_nbrs(width, height):
    dctNbrs = {}
    length = width * height
    for i in range(length):
        dctNbrs[i] = []
        if i - 1 >= 0 and (i - 1) // height == i // height:
            dctNbrs[i].append(i - 1)
        if i + 1 < length and (i + 1) // height == i // height:
            dctNbrs[i].append(i + 1)
        if i + width < length:
            dctNbrs[i].append(i + width)
        if i - width >= 0:
            dctNbrs[i].append(i - width)
    return dctNbrs

# -------------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]
    pzls = open(args[0]).read().splitlines()
    
    goal = pzls[0]
    width, height = dimensions(len(goal))
    
    dct_moves = {-1: "L", 1: "R", -width: "U", width: "D", 0: ""}
    goal_pos_chars = {char: (i // width, i % width) for i, char in enumerate(goal)}
    h_table = build_h_table(goal, width, goal_pos_chars)
    nbrs_table = build_nbrs(width, height)
    
    tasks = [(pzl, goal, width, height, h_table, nbrs_table, dct_moves) for pzl in pzls]
    
    num_processes = max(1, multiprocessing.cpu_count() - 1)
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(solve_and_drul, tasks)
        
    for output in results:
        if output:
            print(output)
