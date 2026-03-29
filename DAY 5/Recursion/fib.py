#Fibonacci 
def fib(n):
    if n<=1:
        return n
    else:
        return fib(n-1)+fib(n-2)
n=int(input())
if n<=0:
    print("invalid")

else:
    print("Fibonacci series")
    for i in range(n):
        print(fib(i))