#Write a program using the built-in max() function to find the largest number in a list
def maxm(*num):
   return max(num)
num=list(map(int, input("Enter numbers separated by space: ").split()))
print("max",max(num))