#10. Data Processing Pipeline
#A data pipeline receives the following array:
#[12, 7, 25, 3, 18, 10]
#Scenario:
#1. Convert the list into a NumPy array.
#2. Sort the array.
#3. Split the sorted array into two equal parts.
#4. Calculate the sum of each part.
#Output:
#● Sorted array
#● Two split arrays
#● Sum of each part
import numpy as np
arr=np.array([12,7,25,3,18,10])
print("Original Array\n",arr)
sort_arr=np.sort(arr)
print("Sorted Array\n",sort_arr)
splt_arr=np.split(arr,2)
print("After splitting into two parts the arrays are\n",splt_arr)
sum_1=np.sum(splt_arr[0])
sum_2=np.sum(splt_arr[1])
print("sum of 1st part",sum_1)
print("sum of 2nd part",sum_2)