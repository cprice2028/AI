import sys; args=sys.argv[1:]
index = int(args[0])
regex_list=["" for _ in range(40)]
regex_list.append(r"/^[x.o]{64}$/i")
regex_list.append(r"/^[xo]*\.[xo]*$/i")
regex_list.append(r"/^(x+o*)?\.|\.(o*x+)?$/i")
regex_list.append(r"/^.(..)*$/s")
regex_list.append(r"/^(0|1[01])([01]{2})*$/")
regex_list.append(r"/\b\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*\b/i")
regex_list.append(r"/^(1?0)*1*$/")
regex_list.append(r"/^[bc]*[abc][bc]*$/")
regex_list.append(r"/^([bc]|a[bc]*a)+$/")
regex_list.append(r"/^(2|1[02]*1)([02]|1[02]*1)*$/")

print(regex_list[index])
num=0
for i in range(40,50):
    num+=len(regex_list[i])
print(num)
'''
Q40: Write a regular expression that will match on an Othello board represented as a string.
Q41: Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
Q42: Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole (assuming it could), it will be connected to one of the corners through X tokens.  Specifically, this means that one of the ends must be a hole, or starting from an end there is a sequence of at least one x followed immediately by a sequence (possibly empty) of o, immediately followed by a hole.
Q43: Match on all strings of odd length.
Q44: Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1.
Q45: Match all words having two adjacent vowels that differ.
Q46: Match on all binary strings which DON'T contain the substring 110.
Q47: Match on all non-empty strings over the alphabet {a, b, c} that contain at most one a.
Q48: Match on all non-empty strings over the alphabet {a, b, c} that contain an even number of a's.
Q49: Match on all positive, even, base 3 integer strings.
'''


#Charlie Price, pd 3, 2028