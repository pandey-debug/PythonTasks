#Write a program that uses random.choice() to randomly select a student from list and display:"The selected student for presentation is: <name>".
import random
l=input("enter students name in list by using ")
s = [name.strip() for name in l.split(",")]
a=random.choice(s)
print("The selected student for presentation is",a)