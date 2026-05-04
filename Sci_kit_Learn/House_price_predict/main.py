import numpy as np
import pandas as pd

ds=pd.read_csv('kc_house_data.csv')
print(ds.head())
X=ds[['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'condition', 'grade', 'sqft_basement', 'yr_built', 'yr_renovated']].values
y=ds['price'].values
print('='*40)
print(f"Shape of X:{X.shape}\n Shape of Y{y.shape}")
# Splitting dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test= train_test_split(X,y,random_state=0,test_size=0.2)
print(f"Length of X_train: {len(X_train)}\nLength of X_test: {len(X_test)}")
print(f"Length of y_train: {len(y_train)}\nLength of y_test: {len(y_test)}")


from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.fit_transform(X_test)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
def evaluate(name,y_test,y_pred):
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    print(f"\n{'='*40}")
    print(f"  {name}")
    print(f"{'='*40}")
    print(f"  MAE  : ${mae:,.0f}")
    print(f"  RMSE : ${rmse:,.0f}")
    print(f"  R2   : {r2:.4f}  ({r2*100:.1f}% variance explained)")

# ============================================================
# 1. Linear Regression
# ============================================================
# Fits a straight line/hyperplane through data by minimizing
# the sum of squared differences between predicted and actual values.
 
from sklearn.linear_model import LinearRegression
 
regressor = LinearRegression()
print(regressor)
 
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
 
evaluate("Linear Regression", y_test, y_pred)
 
 
# ============================================================
# 2. Ridge Regression
# ============================================================
# Linear regression with L2 regularization — penalizes large
# coefficients to reduce overfitting.
 
from sklearn.linear_model import Ridge
 
regressor = Ridge(alpha=1.0)
print(regressor)
 
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
 
evaluate("2. Ridge Regression", y_test, y_pred)
 
 
# ============================================================
# 3. Support Vector Regression (SVR)
# ============================================================
# SVR tries to fit as many data points as possible within an
# epsilon tube around the prediction line.
 
from sklearn.svm import SVR
 
regressor = SVR(kernel='rbf', C=100, epsilon=0.1)
print(regressor)
 
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
 
evaluate("4. Support Vector Regression (SVR)", y_test, y_pred)
 
 
# ============================================================
# 4. Decision Tree Regressor
# ============================================================
# Splits data recursively into branches based on feature values.
# Predicts by averaging target values in each leaf node.
 
from sklearn.tree import DecisionTreeRegressor
 
regressor = DecisionTreeRegressor(max_depth=8, random_state=0)
print(regressor)
 
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
 
evaluate("5. Decision Tree Regressor", y_test, y_pred)
 
 
# ============================================================
# 5. Random Forest Regressor
# ============================================================
# Builds multiple decision trees on random subsets of data and
# averages their predictions — reduces variance and overfitting.
 
from sklearn.ensemble import RandomForestRegressor
 
regressor = RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1)
print(regressor)
 
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
 
evaluate("6. Random Forest Regressor", y_test, y_pred)
 
 
# ============================================================
# 6. Gradient Boosting Regressor
# ============================================================
# Builds trees sequentially — each tree corrects the errors of
# the previous one, boosting overall prediction accuracy.
 
from sklearn.ensemble import GradientBoostingRegressor
 
regressor = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1,
                                      max_depth=4, random_state=0)
print(regressor)
 
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
 
evaluate("7. Gradient Boosting Regressor", y_test, y_pred)




# ============================================================
#               K-Nearest Neighbors Regressor
# ============================================================
from sklearn.neighbors import KNeighborsRegressor

knn=KNeighborsRegressor()
print('-'*80)
print(knn)
#training the model
knn.fit(X_train,y_train)
y_pred=knn.predict(X_test)
# To calculate algorithm score
evaluate("K-Nearest Neighbors Regressor",y_test,y_pred)
 
 # ============================================================
#               Bagging Regressor
# ============================================================
from sklearn.ensemble import BaggingRegressor

bagging_model=BaggingRegressor()
print('-'*80)
print(bagging_model)
#training the model
bagging_model.fit(X_train,y_train)
y_pred=bagging_model.predict(X_test)
#To calculate algorithm score
Model_eval(y_test,y_pred,"Bagging Regressor")

# ============================================================
#               XGBoost Regressor
# ============================================================
from xgboost import XGBRegressor

XGB_model=XGBRegressor()
print('-'*80)
#print(XGB_model)
#training the model
XGB_model.fit(X_train,y_train)
y_pred=XGB_model.predict(X_test)
#To evaluate model 
Model_eval(y_test,y_pred,"XGBoost Regressor")

