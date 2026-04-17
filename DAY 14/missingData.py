#9. Missing Data Handling (NumPy + Pandas)
#A dataset:
#arr = np.array([10, np.nan, 30, np.nan, 50])
#Task:
#● Convert to Pandas Series
#● Replace NaN values with the mean of the Series
#● Print updated data
import numpy as np
import pandas as pd
arr = np.array([10, np.nan, 30, np.nan, 50])
series=pd.Series(arr)
mean_value = series.mean()
series = series.fillna(mean_value)
print(series)