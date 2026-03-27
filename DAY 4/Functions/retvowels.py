#Write a function that takes a string as input and returns the number of vowels.
def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

# Example usage
s = "Hello World"
result = count_vowels(s)
print("Number of vowels:", result)