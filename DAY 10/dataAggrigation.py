#9. Multi-Department Data Aggregation
#A company collects employee counts from two branches.
#Branch A:
#[[10, 20],
#[30, 40]]
#Branch B:
#[[5, 15],
#[25, 35]]
#Scenario:
##● Combine the two matrices.
#● Calculate the total employees across all departments.
#● Print the combined matrix and total.
import numpy as np
arry1=np.array([[10, 20],[30, 40]])
arry2=np.array([[5, 15],[25, 35]])
combined=arry1+arry2
print("Combined matrix",combined)
total=np.sum(combined)
print("Total Matrix",total)

