#6. Matrix Transformation in Image Processing
#An image processing system stores pixel intensity values in a matrix.
#Scenario:
#[[1, 2],
#[3, 4]]
#Task:
#● Create a NumPy array for this matrix.
#● Find its transpose.
#● Print both matrices
import numpy as np
org_arr=np.array([(1,2),(3,4)])
print("Original matrix\n",org_arr)
trspse_arr=np.transpose(org_arr)
print("After Transpose Of Original Matrix is:\n",trspse_arr)

