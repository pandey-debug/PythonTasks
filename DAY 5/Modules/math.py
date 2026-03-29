#Write a Python program using the math module to calculate and display the squareroot, floor value, and ceiling value of a number entered by the user
import math
a=float(input("ENTER A VALUE"))
b=math.ceil(a)
c=math.floor(a)
if a>=0:
    d=math.sqrt(a)
    print("Squareroot value",d)
    
else:
    print("negative value")    
print("ceil value",b)
print("floor value",c)
