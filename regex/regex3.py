import sys; args=sys.argv[1:]
index = int(args[0])
regex_list=["" for _ in range(50)]
regex_list.append(r"/\w*(\w)\w*\1\w*/i")
regex_list.append(r"/\w*(\w)\w*(\1\w*){3}/i")
regex_list.append(r"/^([01])([01]*\1)?$/")
regex_list.append(r"/\b(?=\w*cat)\w{6}\b/i")
regex_list.append(r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i")
regex_list.append(r"/\b(?!\w*cat)\w{6}\b/i")
regex_list.append(r"/\b(?!\w*(\w)\w*\1)\w+/i")
regex_list.append(r"/^(?!.*10011)[01]*$/")
regex_list.append(r"/(?=\w*([aeiou])(?!\1)[aeiou])\w+/i")
regex_list.append(r"/^(?!.*1.1)[01]*$/")

print(regex_list[index])
num=0
for i in range(50,60):
    num+=len(regex_list[i])
print(num)


'''
Q50: Match all words where some letter appears twice in the same word.
Q51: Match all words where some letter appears four times in the same word.
Q52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
Q53: Match all six letter words containing the substring cat.
Q54: Match all 5 to 9 letter words containing both the substrings bri and ing.
Q55: Match all six letter words not containing the substring cat.
Q56: Match all words with no repeated characters.
Q57: Match all binary strings not containing the forbidden substring 10011.
Q58: Match all words having two different adjacent vowels.
Q59: Match all binary strings containing neither 101 nor 111 as substrings.
'''



#Charlie Price, pd 3, 2028