#matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the csv file into a pandas DataFrame
csv = pd.read_csv('./master_scored.csv')

ref_csv = csv.dropna(subset=['Score'])
reduced_csv = pd.DataFrame(ref_csv,columns=['Score','CO2 per mi per seat'])
#print(reduced_csv)

# Assign the data to X and y
# Note: Sklearn requires a two-dimensional array of values
# so we use reshape to create this

X = reduced_csv['Score'].values.reshape(-1, 1)
y = reduced_csv['CO2 per mi per seat'].values.reshape(-1, 1)

#print("Shape: ", X.shape, y.shape)

# Create the model and fit the model to the data

from sklearn.linear_model import LinearRegression

model = LinearRegression()

# Fit the model to the data. 
# Note: This is the training step where you fit the line to the data.

model.fit(X, y)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

# Note: we have to transform our min and max values 
# so they are in the format: array([[ 1.17]])
# This is the required format for `model.predict()`

x_min = np.array([[X.min()]])
x_max = np.array([[X.max()]])

# Calculate the y_min and y_max using model.predict and x_min and x_max

y_min = model.predict(x_min)
y_max = model.predict(x_max)

variables = pd.DataFrame([{'x_min':x_min[0][0],'x_max':x_max[0][0],'y_min':y_min[0][0],'y_max':y_max[0][0]}])

formula = pd.DataFrame([{'Weight Coefficients':model.coef_[0][0],'Y-intercept':model.intercept_[0]}])

formula.to_csv('score_formula.csv',index=False)