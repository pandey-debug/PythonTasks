#largest of three numbers
def find_largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c


num1 = 10
num2 = 25
num3 = 15

largest = find_largest(num1, num2, num3)
print("The largest number is:", largest)