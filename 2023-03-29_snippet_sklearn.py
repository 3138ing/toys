# 미완성
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

X = df['time']
y = df['price_cumsum']
X = np.array(X).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
poly = PolynomialFeatures(degree = 15)

X_train_poly = poly.fit_transform(X_train)

pr = LinearRegression()
pr.fit(X_train_poly, y_train)

X_test_poly = poly.fit_transform(X_test)
y_hat_test = pr.predict(X_test_poly)

fig = plt.figure(figsize = (10, 5))
plt.plot(X_train, y_train, 'o')
plt.plot(X_test, y_hat_test, 'r+')
plt.show()
