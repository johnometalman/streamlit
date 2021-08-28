import pandas as pd
penguins = pd.read_csv('penguins_cleaned.csv')

# Ordinal feature encoding
# https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering

df = penguins.copy()
target = 'species'
encode = ['sex','island']

for column in encode:
    dummy = pd.get_dummies(df[column], prefix=column)
    df = pd.concat([df,dummy], axis=1)
    del df[column]

target_mapper = {'Adelie':0, 'Chinstrap':1, 'Gentoo':2}
def target_encode(val):
    return target_mapper[val]

df['species'] = df['species'].apply(target_encode)

# Separating X and y
X = df.drop('species', axis=1)
Y = df['species']

# Build random forest model
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(X, Y)

# Saving the model
import pickle
pickle.dump(classifier, open('penguins_classifier.pkl', 'wb'))
