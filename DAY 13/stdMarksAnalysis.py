#2. Student Marks Analysis
#Given marks of 5 students in 3 subjects:
#marks = np.array([
#[70, 80, 90],
#[60, 75, 85],
#[50, 65, 70],#
# [90, 95, 85],
#[40, 55, 60]])
#Task:
#● Calculate total marks of each student.
#● Identify students whose total marks are above the class average
import numpy as np
marks = np.array([[70, 80, 90],
[60, 75, 85],
[50, 65, 70],
[90, 95, 85],
[40, 55, 60]])
sum_marks = np.sum(marks, axis=1)
print(sum_marks)
mean_marks=np.mean(sum_marks)
print("average",mean_marks)
above_avg=sum_marks[sum_marks>mean_marks]
print(above_avg[0])