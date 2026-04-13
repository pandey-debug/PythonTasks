#1. Fruit Sales Comparison (Series Addition)
#A shop tracks fruit sales:
#S1 = pd.Series([10, 20, 30], index=["apple", "banana", "cherry"])
#S2 = pd.Series([5, 15, 25], index=["apple", "banana", "cherry"])
#Task:
#● Add both series
#● Find the total sales of all fruits combined
import pandas as pd
import numpy as np
S1=pd.Series([10, 20, 30], index=["apple", "banana", "cherry"])
S2=pd.Series([5, 15, 25], index=["apple", "banana", "cherry"])
add=S1+S2
summ=np.sum(add)
print("sum",summ)
print("After Adding Two Series\n",add)
