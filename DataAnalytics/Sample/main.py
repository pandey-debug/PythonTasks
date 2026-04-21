import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
df=pd.read_csv('railway_gauges.csv')
df.head()
print(df.head())

print(df.iloc[[df['Total'].idxmax()]])
df=df.drop('Total',axis=1)
ax=df.plot(x="Year", kind="bar")
plt.xticks(rotation=70)
plt.xlabel('Year')
plt.ylabel('Total')
plt.title('Gauges: Number of railway tracks installed per year')
plt.savefig('rail_gauge.png')
plt.show()