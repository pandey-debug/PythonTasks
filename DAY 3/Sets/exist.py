
 
a=input("ENTER NUMBRES IN A SET ")
s=set(map(int,a.split()))
print(s)
e=int(input("Enter a number to search"))
if e in s:
    print("element found")


else:print("not found")
