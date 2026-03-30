def checkPrimeNum(Num):
    if Num<=1:
        print(f"{Num} is not a Prime Number")
        return
   
    for i in range(2,Num//2+1):  # range(2,int(Num**0.5)+1)
        if Num%i==0:
            print(f"{Num} is not a Prime Number")
            return
    print(f"{Num} is a Prime Number")
       
try:
    Num=int(input("Enter a positive Number:"))
    checkPrimeNum(Num)
except ValueError:
    print("Enter an Integer value!")
    