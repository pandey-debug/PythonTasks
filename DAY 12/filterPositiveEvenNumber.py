#7. Filter Positive Even Numbers from Dataset
#Scenario:
#A dataset contains mixed values:
#arr = [-5, 10, 15, -2, 20, 25, 30]
#Task:
#● Convert to NumPy array.
#● Filter values that are:
#○ Positive
#○ Even
import numpy as np
arr=np.array([-5, 10, 15, -2, 20, 25, 30])
new_arr=arr[(arr>0)&(arr % 2 == 0)]
print(new_arr)
