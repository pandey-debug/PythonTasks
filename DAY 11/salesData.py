#8. Iterate Through Daily Sales
#Daily sales data:
#[200, 300, 150, 400]
#Task:
#● Store it in a NumPy array.
#● Iterate through the array and print each sale value.
import numpy as np
sales_data=np.array([200,300,150,400])
for x in np.nditer(sales_data):
    print(x)