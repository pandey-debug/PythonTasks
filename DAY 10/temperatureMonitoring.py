#Temperature Monitoring System
#A weather station records temperatures for two days.
#Scenario:
#Day 1: [30, 32, 31]
#Day 2: [29, 33, 34]
#Task:
#● Create a 2D NumPy array to store this data.
#● Print the array.
#● Find the total temperature recorded.
import numpy as np
temp_data=np.array([(30,32,31),(29,33,34)])

print(temp_data)
temp_data=np.sum(temp_data)  # or we can give other variable like summ=np.sum(temp_data) 
print("Total of Temperture Recorded is:",temp_data)