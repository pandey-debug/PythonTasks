#4. Combine Two Sensor Readings
#Two sensors record readings during a test.
#Scenario:
#Sensor1 = [10, 20, 30]
#Sensor2 = [40, 50, 60]
#Task:
#● Store both readings in NumPy arrays.
#● Combine them into one array using NumPy concatenation.
import numpy as np 
sensor1=np.array([10,20,30])
sensor2=np.array([40,50,60])
final=np.concatenate((sensor1,sensor2))
print("after concatination:",final)





