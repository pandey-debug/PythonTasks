#6. Multi-Level List Transformation (Advanced List Comprehension)
#A dataset contains:
#data = [[1, 2, 3], [4, 5], [6]]
#Task:
#● Flatten the list using list comprehension.
#● Then create a new list containing squares of only even numbers.
data = [[1, 2, 3], [4, 5], [6]]
new_lst=[x for sublist in data for x in sublist]
print(new_lst)