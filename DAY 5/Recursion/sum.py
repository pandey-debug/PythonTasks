#Write a recursive function to calculate the sum of digits of a number
def summ(s):
    if s ==0:
        return 0
    else:
        return  (s % 10) + summ(s//10)

a=int(input("enter a string"))
b=summ(a)    
print(b)