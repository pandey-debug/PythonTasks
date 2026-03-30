def checkpalindromeNum(Num):
    original=Num
    sum_p=0
    while(Num>0):
        a=Num%10
        sum_p=sum_p*10+a
        Num=Num//10
    if original==sum_p:
        print(f"{original} is a Palindrome Number")
    else:
        print(f"{original} is not a Palindrome Number")
 
try:
    Num=int(input("Enter a number:"))
    if Num<0:
        print("Enter a positive Number")
    else:
        checkpalindromeNum(Num)
except ValueError:
    print("Enter a valid Integer!")