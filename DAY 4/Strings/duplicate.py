#Write a program to remove duplicate characters from a string.
string = input("Enter a string: ")
b = ""

for char in string:
    if char not in b:
        b += char

print("String after removing duplicates:", b)