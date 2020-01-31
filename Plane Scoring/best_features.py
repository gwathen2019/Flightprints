# Feature Selection with Univariate Statistical Tests
from pandas import read_csv
from numpy import set_printoptions
import numpy as np
from sklearn.feature_selection import *
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from keras.utils import to_categorical

# load data
filename = 'master_scored_ML.csv'

dataframe = read_csv(filename)
dataframe = dataframe.drop(columns=['Sector','CO2 per mi','Fuel per seat','Score'])

dataframe['Fuel burn'] = dataframe['Fuel burn'].str.split('k').str[0].astype(float)
#dataframe['Fuel per seat'] = dataframe['Fuel per seat'].str.split('L').str[0].astype(float)
dataframe['Model'] = dataframe['Model'].str.split(' ').str[0]
dataframe = dataframe[['First flight', 'Fuel burn', 'Max Range', 'Seats', 'Model', 'CO2 per mi per seat']]
#dataframe = dataframe[['First flight', 'Max Range', 'Model', 'Fuel per seat']]

# Step 1: Label-encode data set
label_encoder = LabelEncoder()
label_encoder.fit(dataframe['Model'])
encoded_y = label_encoder.transform(dataframe['Model'])

for label, original_class in zip(encoded_y, dataframe['Model']):
    print('Original Class: ' + str(original_class))
    print('Encoded Label: ' + str(label))
    print('-' * 12)

# Step 2: One-hot encoding
one_hot_y = to_categorical(encoded_y)
dataframe['Model']=one_hot_y

array = dataframe.values
X = array[:,0:5]
Y = array[:,5]

# Feature extraction
# Using Pearson’s Correlation Coefficient
test = SelectKBest(score_func=f_regression, k=4)
fit = test.fit(X, Y)

# Summarize scores
set_printoptions(precision=3)
for i in range(0,len(fit.scores_)):
    print(fit.scores_[i])
features = fit.transform(X)

# Summarize selected features
print(features[0:10,:])