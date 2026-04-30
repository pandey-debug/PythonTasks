#X= 7a + 3b + 4c + 9c
from random import randint
from sklearn.linear_model import LinearRegression
train_set_limit=1000
train_set_count=100
TRAIN_INPUT=list()
TRAIN_OUTPUT=list()
for i in range(train_set_count):
    a=randint(0,train_set_limit)
    b=randint(0,train_set_limit)
    c=randint(0,train_set_limit)
    d=randint(0,train_set_limit)
    res=(7*a) + (3*b) + (4*c) + (9*d)
    TRAIN_INPUT.append([a,b,c,d])
    TRAIN_OUTPUT.append(res)
predictor=LinearRegression(n_jobs=-1)
predictor.fit(X=TRAIN_INPUT,y=TRAIN_OUTPUT)

x=[[1,2,3,4]]
op=predictor.predict(X=x)
coeff=predictor.coef_
print(op,coeff)