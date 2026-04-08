#3. Sorting Product Prices
#An e-commerce company stores product prices in a NumPy array.
#Scenario:
#Prices = [499, 299, 799, 199, 599]
#Task:
#● Convert it into a NumPy array.
#● Sort the prices in ascending order.
import numpy as np
Prices = [499, 299, 799, 199, 599]
Prices=np.array(Prices)
Prices=np.sort(Prices)   #Used same name because it overrides the varaiables present above:
print(Prices)