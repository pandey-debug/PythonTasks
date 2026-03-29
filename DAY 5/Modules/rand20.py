#Write a Python program that generates 20 random numbers between 1 and 200 using
#the random module and store them in a list.Then using the math module, compute and display:
# ● Maximum value● Minimum value● Square root of the maximum number● Logarithm of the minimum number
import random
import math
a=[random.randint(1,200)for a in range(20)]# List comprehension
print(a)
print("Max Value of list is",max(a))
print("Min Value of list is",min(a))
for i in a:
    if i== max(a):
     print(" Square Root of Max Value of list is",(math.sqrt(i)))

for i in a:
   if i==min(a):
      print("Log Value of min Value of list is",(math.log(i)))
#OR
#b=max(a)
#c=min(a)
#print("Log Value of min Value of list is",(math.log(c)))
#print("sqrt Value of max Value of list is",(math.sqrt(b)))
#print("Max Value of list is",b)
#print("Min Value of list is",c)



