def string_times(str, n): return str*n #$
def front_times(str, n):  return str[:3]*n #$
def string_bits(str): return str[::2] #$
def string_splosion(k): return  "".join([k[:i+1] for i in range(len(k))])#^
def last2(k):return sum([ 1 for n in range(len(k)-2) if k[n:n+2] == k[-2:]])#^
def array_count9(nums): return nums.count(9)#$
def array_front9(nums):return 9 in nums[:4]#$
def array123(nums):return [1,2,3] in [nums[n:n+3] for n in range(len(nums)-2)]#^
def string_match(a, b): return sum([a[i:i+2] == b[i:i+2] for i in range(len(a)-1)]) # ^ 
def make_bricks(small, big, goal):  return ((big*5+small)>=goal) and (small>=goal%5)#^
def lone_sum(a, b, c): return sum([n for n in [a,b,c] if [a,b,c].count(n)==1])#^
def lucky_sum(a, b, c): return sum([a,b,c][n] for n in [a,b,c] if 13 not in [a,b,c][:n+1])#1 updated
def no_teen_sum(a, b, c): return sum(v for v in [a,b,c] if not (13<=v<=14 or 17<=v<=19))#^
def round_sum(a, b, c): return sum(([a,b,c][n]+5)//10*10 for n in range(3))#^
def close_far(a, b, c): return any(abs(x-y)<=1 and abs(x-z)>=2 and abs(y-z)>=2 for x,y,z in [(a,b,c),(a,c,b)]) #1
def make_chocolate(small, big, goal):return [l for l in [[0]] if (((goal>=5*big and l.append(goal-5*big)) or ( goal<=5*big and l.append(goal%5))) or (l[1]>small and (l.pop(0) or l.append(-1))) or True)][0][-1]#1
def double_char(k): return "".join(s*2 for s in k)#$
def count_hi(k):return k.count('hi')#$
def cat_dog(k):return k.count('cat')==k.count('dog')#^
def count_code(k): return sum([k[n:n+2]=="co" and k[n+3]=="e" for n in range(len(k)-3)])#^
def end_other(a, b): return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())#^
def xyz_there(k): return "xyz" in [k[n:n+3] for n in range(len(k)) if n==0 or k[n-1]!='.']#1
def count_evens(nums):return sum([n%2==0 for n in nums])#^
def big_diff(nums):return max(nums)-min(nums)#$
def centered_average(nums): return (sum(nums)-max(nums)-min(nums))//(len(nums)-2)#^
def sum13(nums): return sum([val for n,val in enumerate(nums) if val!=13 and (n==0 or nums[n-1]!=13)])#^
def sum67(nums): return sum(n for skip in [[False]] for n in nums if (n==6 and (skip.append(True) or skip.pop(0)) and False) or (not skip[0]) or ((n==7 and (skip.append(False) or skip.pop(0))) and False))#1
def has22(nums):return (2,2) in zip(nums,nums[1:]) #$
#$$$^^$$1^^11^^11$$^^^1^$^^11
#$$$^^$$^^^^1^^11$$^^^1^$^^11
#$$$^^$$^^^^1^^11$$^^^1^$^^1$
#Charles Price, 3, 2028