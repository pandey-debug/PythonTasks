#� Scenario 1: Basic Data Loading & Cleaning
#You are given a CSV file containing railway gauge data.
#�� Tasks:
#1. Load the dataset into a Pandas DataFrame.
#2. Display the first 5 rows and column names.
#3. Check for missing values and replace them with 0.
#4. Convert all gauge columns (Broad, Metre, Narrow, Total) to numeric types.


#Lets import the required packages and modules first
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Loading the .Csv file to process the data
df=pd.read_csv('railway_gauges1.csv')
df.columns = df.columns.str.strip()
#print(df)#for confirmation of data set



#Processing the first 5 rows and colunms names
print("First Five ROWS ")
print(df.head())#df.head() gives the first 5 frowswith data
#column Names
print("The COLUMN Names")
print(df.columns)


#Check for missing values and replace them with 0.
#it checkes the data is null or not  and if null it provides true else false
print(df.isnull().sum()) 
df=df.fillna(0)
#print(df)



#Convert all gauge columns (Broad, Metre, Narrow, Total) to numeric types.
gauge_columns = ['Broad Gauge', 'Metre Gauge', 'Narrow Gauge', 'Total']
for col in gauge_columns:
    df[col]=pd.to_numeric(df[col],errors='coerce').fillna(0)
print("\nData types after conversion:")
print(df.dtypes)    




#Scenario 2: Simple Visualization
#You want a quick understanding of total railway track growth.
#�� Tasks:
#1. Extract Year and Total columns.
#2. Plot a line graph showing Total tracks over years.
#3. Add:
#○ Title
#○ X and Y labels
#4. Identify whether the trend is increasing or decreasing
df['Year'] = df['Year'].str[:4].astype(int)
year=df['Year']
total=df['Total']
plt.plot(year,total)
plt.xlabel("YEAR")# This labels Year in the x axis
plt.ylabel("Total")# this labesl Total in y axis
plt.title("RAILWAY TRACK GROWTH")
plt.grid(True)#this give sthe grid ,this 
plt.savefig("trend.png")#saving the line graph using this
plt.show()



#Scenario 3: Filtering + Bar Chart
#You are asked to analyze modern railway expansion.
#�� Tasks:
#1. Filter the dataset for years after 2000.
#2. Select Broad Gauge, Metre Gauge, and Narrow Gauge.
#3. Plot a grouped bar chart comparing all three gauges.
#4. Add legend and proper labels.
#5. Identify which gauge dominates in recent years.

# Filter years after 2000
df['Year_start']=df['Year']
df_recent = df[df['Year'] > 2000]

# Data
year=df_recent['Year']
broad=df_recent['Broad Gauge']
metro=df_recent['Metre Gauge']
narrow=df_recent['Narrow Gauge']

# Positions
x=np.arange(len(year))
#plt.figure(figsize=(12,6))

plt.bar(x-0.2,broad,width=0.2,label='Broad Gauge')
plt.bar(x,metro,width=0.2,label='Metre Gauge')
plt.bar(x+0.2,narrow,width=0.2,label='Narrow Gauge')

plt.xticks(x, year, rotation=45)

plt.xlabel("Year")
plt.ylabel("Track Length")
plt.title("Railway Gauge Comparison > 2000")
plt.legend()
plt.savefig('bar.png')#saving the figure ie bar graph
plt.show()


#Scenario 4: Feature Engineering + Pie Chart
#You want to analyze the contribution of each gauge type.
#1. Calculate total sum of each gauge across all years.
#2. Create a new structure (Series/DataFrame) for totals.
#3. Plot a pie chart showing percentage contribution.
#4. Add percentage labels (autopct).
#5. Interpret which gauge contributes the most.
g_columns=['Broad Gauge','Metre Gauge','Narrow Gauge']
total=df[g_columns].sum()
#Creating  a new structure for totals
total_df = pd.DataFrame(total, columns=['Total'])
print(total_df)
plt.figure(figsize=(6,6))


plt.pie(total,labels=total.index,autopct='%1.1f%%', startangle=90)
# 4. Add title
plt.title('Gauge Contribution(%)')

# Equal aspect ratio ensures pie is drawn as a circle
plt.axis('equal')
plt.savefig('pie.png')
plt.show()






#Scenario 5: Advanced Analysis + Multiple Graphs
#You are asked to perform a complete analysis of railway trends.
#�� Tasks:
#1. Create new columns:
#○ % Broad Gauge
#○ % Metre Gauge
#○ % Narrow Gauge
#2. Use NumPy (np.diff) to calculate yearly growth of Total tracks.
#3. Plot:
#○ Line graph for all gauge

#we have the formula to convert into percentage as (x/total)*100
df['(%)Broad Gauge']=(df['Broad Gauge']/df['Total'])*100
df['(%)Metre Gauge']=(df['Metre Gauge']/df['Total'])*100
df['(%)Narrow Gauge']=(df['Narrow Gauge']/df['Total'])*100


#calculating yearly growth
df['Yearly Growth'] = np.diff(df['Total'],prepend=df['Total'].iloc[0])



plt.figure(figsize=(10,6))

plt.plot(df['Year'], df['Broad Gauge'], marker='o', label='Broad Gauge')
plt.plot(df['Year'], df['Metre Gauge'], marker='o', label='Metre Gauge')
plt.plot(df['Year'], df['Narrow Gauge'], marker='o', label='Narrow Gauge')

plt.xlabel('Year')
plt.ylabel('Track Length')
plt.title('Railway Gauge Trends Over Years')
plt.legend()
plt.grid(True)
plt.savefig('final.png' )

plt.show()
