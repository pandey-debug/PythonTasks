#Write a function to find the sum of elements in a list using a user-defined function.def find_sum(numbers):
def summ(numbers):
    total = 0
    for num in numbers:
        total += num
    return total


listt = [1, 2, 3, 4, 5]
result = summ(listt)
print("Sum of elements:", result)