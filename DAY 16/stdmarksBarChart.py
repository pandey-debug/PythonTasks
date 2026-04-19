#2. Student Marks Bar Chart
#Scenario:
#Marks of students:
#names = ["A", "B", "C", "D"]
#marks = np.array([70, 85, 60, 90])
#Task:
#● Create a DataFrame
#● Plot a bar graph
#● Show student names on X-axis
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
names = ["A", "B", "C", "D"]
marks = np.array([70, 85, 60, 90])
df=pd.DataFrame({"Names":names,"Marks":marks})
print(df)
plt.bar(df["Names"],df["Marks"])
plt.xlabel("names")
plt.ylabel("marks")
plt.title("Student Marks")
plt.show()

