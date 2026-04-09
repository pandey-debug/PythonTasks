#15. Reshape and Flatten Image Data
#Scenario:
#An image is stored as a 2 × 3 matrix:
#[[1,2,3],
#[4,5,6]]
#Task:
#1. Convert it into a NumPy array.
#2. Flatten the array into 1-D format.
#3. Print the flattened array
import numpy as np
data=np.array([[1,2,3],[4,5,6]])
new_data=data.reshape(-1)
print("NEW ARRAY:",new_data)
