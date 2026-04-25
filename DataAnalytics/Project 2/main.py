#==============================================================================================
#Lets import the required modules
#==============================================================================================
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#==============================================================================================
#Scenario 1: Basic Data Loading & Cleaning (🟢 Easy)
#==============================================================================================
#1.	#Load the ign.csv dataset using Pandas.
#2.	Display the first 5 rows (head()), last 5 rows (tail()), and the shape of the dataset.
##3.	Remove the unnecessary column: "Unnamed: 0".
#4.	Check for missing values in score, genre, and platform.
#5.	Handle missing values: Fill the numeric column score with the mean, and the categorical column genre with the mode.
#6.	Ensure correct data types: Convert score → float and release_year, release_month, release_day → integer.
df=pd.read_csv('ign.csv')
print("Displaying First Five Rows")
print(df.head())#for first 5 rows data
print("Displaying Last Five  Rows")
print(df.tail())# for last 5  rows data
df=df.drop(columns=['Unnamed: 0'])#removes the unnecessary column
print(df.head())
print(df[['score', 'genre', 'platform']].isnull().sum())#for missing values
df['score']=df['score'].fillna(df['score'].mean())#filled the missinge values in score and genrewith mean and mode respectively
df['genre']=df['genre'].fillna(df['score'].mode())
df['score']=df['score'].astype(float)
df['release_year']=df['release_year'].astype(int)#astype converts into required datatype
df['release_month']=df['release_month'].astype(int)
df['release_day']=df['release_day'].astype(int)
print(df.dtypes)

#==============================================================================================
#Scenario 2: Line Graph (Score Trend) + Save (🟢 Easy)
#==============================================================================================
'''1.	Group data by release_year.
2.	Calculate the average score per year using Pandas.
3.	Convert the resulting average scores and years into NumPy arrays.
4.	Plot a line graph with release_year on the X-axis and average score on the Y-axis.
5.	Add the title: "Average Game Score Over Years" and proper axis labels.
6.	Save the graph: plt.savefig("avg_score_trend.png").
'''
avg_score=df.groupby('release_year')['score'].mean().reset_index()
avgnp=avg_score['score'].to_numpy()
releaseYear_np=avg_score['release_year'].to_numpy()
print(avg_score)
plt.plot(releaseYear_np,avgnp, marker='o')
plt.xlabel('Release Year')
plt.ylabel('Average Score')
plt.title("Average Game Score Over Years" )
plt.savefig("avg_score_trend.png")
plt.show()

#==============================================================================================
#Scenario 3: Filtering + Bar Chart + Save (🟡 Medium)
#==============================================================================================
'''1.	Filter the dataset to include only games where score > 7.
2.	Count the number of high-rated games per platform.
3.	Select the top 10 platforms using Pandas.
4.	Convert the platform counts into NumPy arrays.
5.	Plot a bar chart with platform on the X-axis and count of games on the Y-axis.
6.	Rotate x-axis labels for readability.
7.	Save the graph: plt.savefig("top_platforms_bar.png").
'''
fil_df=df[df['score']>7]
#print(fil_df)
high_val=fil_df['platform'].value_counts()
selected_val=high_val.head(10)
print(selected_val)
platform_names=selected_val.index.to_list()
game_count=selected_val.to_numpy()
plt.bar(platform_names,game_count)
plt.xlabel('Platform')
plt.ylabel('Count of games')
plt.xticks(rotation=60)
plt.title("Counts")
#plt.tight_layout()
plt.show()
plt.savefig('top_platforms_bar.png')
#==============================================================================================
#Scenario 4: Aggregation + Pie Chart + Save (🟡 Medium)
#==============================================================================================
'''1.	Count the total number of games per genre.
2.	Select the top 5 genres using Pandas.
3.	Prepare labels (genres) and values (counts) for the pie chart.
4.	Plot a pie chart using genre as labels and count as values.
5.	Add percentage labels using autopct (e.g., '%.1f%%').
6.	Save the graph: plt.savefig("genre_distribution.png").
'''
genre_count=df['genre'].value_counts()
top_genre=genre_count.head(5)
print(top_genre)
label=top_genre.index
values=top_genre.to_numpy()
plt.pie(values,labels=label, autopct='%.1f%%')
plt.axis('equal')
plt.savefig("genre_distribution.png")
plt.show()
#==============================================================================================
#Scenario 5: Advanced Analysis + Multiple Graphs (🔴 Hard)
#==============================================================================================
'''1.	Create a new column score_category: "Excellent" for score $\ge 9$, "Good" for $7 \le$ score $< 9$, and "Average" for score $< 7$.
2.	Convert the editors_choice column: 'Y' $\rightarrow 1$, 'N' $\rightarrow 0$.
3.	Use NumPy's np.diff() to calculate the yearly score growth based on the average yearly scores from Scenario 2.
4.	Plot a Line Graph showing the trend of average score per release_year.
5.	Plot a Stacked Bar Chart showing the count of score_category per release_year.
'''
condition=[df['score']>=9,( df['score']>=7) & (df['score']<9), df['score']<7]
choose=['Excellent','Good','Average']
df['score_category']=np.select(condition,choose,default='Unknown')
df['editors_choice']=df['editors_choice'].map({'Y':1,'N':0})
avg_yearly=df.groupby('release_year')['score'].mean().sort_index()
score_growth=np.diff(avg_yearly.values)
plt.figure(figsize=(8, 5))
plt.plot(avg_yearly.index, avg_yearly.values, marker='o')
plt.title('Average Score per Release Year')
plt.xlabel('Release Year')
plt.ylabel('Average Score')
plt.grid(True)
plt.savefig('final.png')
plt.show()

