#2. Even Number Filter (List Comprehension)
#A system stores numbers:
#nums = [1, 2, 3, 4, 5, 6]
#Task:
#● Use list comprehension to create a new list containing only even numbers.
num=[1, 2, 3, 4, 5, 6]
new_num=[x for x in num if x % 2 == 0 ]
print(new_num)



