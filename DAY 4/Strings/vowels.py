#Write a program to count the number of vowels in a string.
s="aeiouAEIOU"
s1=input("ENTER A STRING TO CHECK")
c=0
for char in s1:
    if char in s:
        c+=1

print("Total vowels are ",c)