#5. Write a program to assign grades based on marks (for example: A, B, C, Fail).
a=int(input("ENTER PERCENTAGE"))
if a>90:
    print("PASS,First class , GRADE A")
elif a>80:
    print("PASS,Second class, GRADE B")

elif a>=45:
    print("PASS,Third class, GRADE C")
else:
    print("FAIL")