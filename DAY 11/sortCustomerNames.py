#12. Sorting Customer Names
#A system stores customer names:
#["Ravi", "Anil", "Sita", "John"]
#Task:
#● Convert it to a NumPy array.
#● Sort the names alphabetically
import numpy as np 
cstmr_names=np.array(["Ravi", "Anil", "Sita", "John"])
print("Sorted",np.sort(cstmr_names))