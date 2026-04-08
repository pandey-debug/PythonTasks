#1. Student Marks Analysis
#A teacher stores the marks of 5 students in a NumPy array.
#Scenario:
#You are given marks [45, 67, 89, 56, 72].
#Task:
#● Convert the list into a NumPy array.
#● Add 5 grace marks to every student.
#● Print the updated marks.


import numpy as np
std_mrks=np.array([45, 67, 89, 56, 72])
print("Before Adding Student Marks are\n")
print(std_mrks,"\n")
std_mrks+=5
print("After Adding +5 Marks for student \n")
print(std_mrks,"\n")

