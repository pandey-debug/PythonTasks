#LETS import the libraries
import numpy as np
import pandas as pd

#loading the dataset
ds=pd.read_csv("Iris.csv")
print(ds.head())
# Selecting features (X) and target (y)
X=ds[['SepalLengthCm','PetalLengthCm','SepalWidthCm','PetalWidthCm']].values
y=ds['Species'].values
print('-'*40)
print(f"Shape of X:{X.shape}\n Shape of y:{y.shape}")



# Splitting dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(   #
    X, y, test_size=0.2, random_state=0
)




print(f"Length of X_train: {len(X_train)}\nLength of X_test: {len(X_test)}")
print(f"Length of y_train: {len(y_train)}\nLength of y_test: {len(y_test)}")
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()#StandardScaler is used to standardize features by removing the mean and scaling to unit variance.
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
 #============================================================
# 1. Support Vector Machine (SVM)
# ============================================================
# SVM tries to find the best boundary (line/plane) to separate classes.
# It focuses on maximizing the margin between different classes.
from sklearn.svm import SVC
classifier=SVC()
classifier.fit(X_train,y_train) # this is for training the model with data
y_pred=classifier.predict(X_test)
 
from sklearn.metrics import accuracy_score
print("="*40) 
print("{:.0%}".format(accuracy_score(y_test,y_pred)))
# Evaluate accuracy



# ============================================================
# 2. Logistic Regression
# ============================================================
# Logistic Regression predicts probability and classifies using a threshold.
# It works well for linearly separable data.

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 3. Naive Bayes
# ============================================================
# Naive Bayes assumes features are independent of each other.
# It uses probability to predict the most likely class.

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 4. Decision Tree Classifier
# ============================================================
# Decision Tree splits data into branches based on feature values.
# It makes decisions like a flowchart.

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 5. Random Forest Classifier
# ============================================================
# Random Forest builds multiple decision trees and combines their results.
# It improves accuracy and reduces overfitting.

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))
