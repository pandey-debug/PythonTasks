#Write a program to find the largest of three numbers using if-elif-else.
a,b,c=map(int,input("ENTER THREE NUMBERS").split())
if a>b and a>c:
    print(f"A={a} is greatest")
elif b>c and b>a:
     print(f"B={b} is greatest")
else:
     print(f"C={c} is greatest")     
