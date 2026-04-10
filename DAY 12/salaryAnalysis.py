#11. Boolean Masking for Salary Analysis
#Scenario:
#Employee salaries:
#[25000, 40000, 15000, 50000, 30000]
#Task:
#● Filter salaries above 30000.
#● Count how many employees satisfy this condition.
import numpy as np
salaries=np.array([25000,40000,15000,50000,30000])
filtered=salaries[salaries>30000]
print("Salaries above 30000:",filtered)
count=filtered.size
print("Count:",count)
