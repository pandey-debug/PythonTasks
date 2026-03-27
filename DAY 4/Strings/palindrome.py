#Write a program to check whether a string is a palindrome
s=input("Enter A Palindrome")
c=s.lower()
#or s.upper()
s2=c[::-1]
if c==s2:
    print("The given String is palindrome\n")

else:
    print("The Given String is Not A Palindrome")    