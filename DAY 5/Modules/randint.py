#Write a Python program using the random module to generate 10 random integersbetween 1 and 100 and store them in a list. Print the lisfro
from random import randint
a=[randint(1,100)for a in range(10)]# List comprehension
print(a)
