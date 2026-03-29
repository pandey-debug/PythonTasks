#Write a recursive function to reverse a string.
def revv(s):
    if len(s)== 0:
      return 0
    else:
       return s[1:]+s[0]
    
d=input("Enter a string")    
rev=revv(d)
print("",d)
print("",rev)