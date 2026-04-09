#13. Copy vs View Behavior in Data Processing
#Scenario:
#A dataset:
#[10, 20, 30, 40]
##Task:
#● Create a copy of the array.
#● Modify the original array.
#● Show that the copy does not change.
#● Repeat using view() and observe the difference.
import numpy as np
org_array=np.array([10,20,30,40])
cpy_array=org_array.copy()
print(cpy_array)
view_array=org_array.view()
view_array[3]=1
print(view_array)
print(org_array)