import numpy as np
import pandas as pd 
from sklearn.linear_model import LinearRegression

df = pd.read_csv("./data/sodium.csv")

Xt = df[['sodium', 'age', 'proteinuria']]
y = df['sbp']
model = LinearRegression()
model.fit(Xt, y)

Xt1 = pd.DataFrame.copy(Xt)
Xt1['sodium'] = 1
Xt0 = pd.DataFrame.copy(Xt)
Xt0['sodium'] = 0
ate_est = np.mean(model.predict(Xt1) - model.predict(Xt0))
print('ATE estimate:', ate_est)