#8. Inventory Update System
#A warehouse has an inventory stored in a matrix.
#[[10, 15],
#[20, 25]]
#Scenario:
#A new shipment increases every item quantity by 2 units.
#Task:
#● Add 2 to every element using NumPy.
#● Print the updated inventory.
import numpy as np
arr=np.array([[10, 15],[20, 25]])
arr=arr+2
print(arr)
