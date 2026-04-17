#4. Find Maximum Value
#A dataset:
#arr = np.array([12, 45, 22, 67, 34])
#Task:
#● Convert to Pandas Series
#● Find the maximum value
import numpy as np
import pandas as pd
arr=np.array([12, 45, 22, 67, 34])
arr=pd.Series(arr)
max_value = arr.max()
print(arr)
print("MAX VALUE FROM SERIES :",max_value)

