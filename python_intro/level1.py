#warmup1
def sleep_in(weekday, vacation):  return (vacation or not weekday)
def monkey_trouble(a_smile, b_smile):  return a_smile == b_smile
def sum_double(a, b): return 2*(a+b) if a == b else a + b
def diff21(n): return 2*abs(21-n) if n > 21 else abs(21-n)   
def parrot_trouble(talking, hour): return True if(talking and (hour<7 or hour>20)) else False
def makes10(a, b): return (a==10 or b==10 or a+b==10)
def near_hundred(n): return abs(100-n)<=10 or abs(200-n)<=10
def pos_neg(a, b, negative): return a<0 and b<0 if negative else a<0 and b>0 or b<0 and a>0
#string1
def hello_name(name): return 'Hello ' + name +'!'
def make_abba(a, b): return a +b +b+a
def make_tags(tag, word): return "<"+tag+">"+word+"</"+tag+">"
def make_out_word(out, word): return out[:len(out)//2]+word+out[len(out)//2:]
def extra_end(str): return str[-2:]*3
def first_two(str): return str if len(str) <2 else str[:2]
def first_half(str): return str[:len(str)//2]
def without_end(str): return str[1:-1]
#list1
def first_last6(nums):  return  (nums[0] == 6 or nums[-1] == 6) or (nums[0] == "6" or nums[-1] == "6")
def same_first_last(nums):  return (len(nums)>=1 and nums[0]==nums[-1])
def make_pi(n): return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]
def common_end(a, b):  return a[0]==b[0] or a[-1]==b[-1]
def sum3(nums): return sum(nums)
def rotate_left3(nums): return nums[1:]+[nums[0]]
def reverse3(nums): return nums[::-1]
def max_end3(nums): return [max(nums[0],nums[-1])]*len(nums)
#logic1
def cigar_party(cigars, is_weekend):  return cigars>=40 if is_weekend else  cigars>=40 and cigars<=60
def date_fashion(you, date): return 0 if you <=2 or date <=2 else 2 if you >= 8 or date >= 8  else 1
def squirrel_play(temp, is_summer):  return temp >=60 and temp<=100 if is_summer else temp >=60 and temp <=90 
def caught_speeding(speed, is_birthday):  return 0 if speed <= (65 if is_birthday else 60) else 1 if speed <= (85 if is_birthday else 80) else 2
def sorta_sum(a, b):  return 20 if a+b<=19 and a+b>=10 else a+b
def alarm_clock(day, vacation): return "off" if (day == 6 or day == 0) and vacation else "10:00" if vacation or day == 6 or day == 0 else "7:00"
def love6(a, b): return a == 6 or b == 6 or a +b ==6 or a - b ==6 or b- a==6
def in1to10(n, outside_mode): return n <=1 or n>=10 if outside_mode else n>=1 and n<=10
#Charles Price, pd. 3 , 2028