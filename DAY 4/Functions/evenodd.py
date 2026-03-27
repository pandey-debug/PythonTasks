def check_even_odd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Taking input from user
number = int(input("Enter a number: "))

# Calling the function
result = check_even_odd(number)
print(f"{number} is {result}")