def checkArmstrongNum(Num):
    original=Num
    sum_digits=0
    while(Num>0):
        a=Num%10
        sum_digits+=a**3
        Num=Num//10
    if original==sum_digits:
       print(f"{original} is Armstrong Number!")
    else:
        print(f"{original} is not an Armstrong Number!")        
 
try:
   Num=int(input("Enter a positive integer:"))
   checkArmstrongNum(Num)
except ValueError:
    print("Enter a valid Integer!")