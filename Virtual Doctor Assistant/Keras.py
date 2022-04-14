# %% [code]
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import warnings

warnings.filterwarnings('ignore')

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code]
train = pd.read_csv('/kaggle/input/disease-prediction-using-machine-learning/Training.csv')
test = pd.read_csv('/kaggle/input/disease-prediction-using-machine-learning/Testing.csv')
train.head()

# %% [code]
test.head()

# %% [code]
train.shape

# %% [code]
test.shape

# %% [code]
train.drop('Unnamed: 133', axis=1, inplace=True)
train.shape

# %% [code]
train.info()

# %% [code]
train.isna().sum()

# %% [code]
train.nunique()

# %% [code]
X_train = train.drop('prognosis', axis=1)
X_test = test.drop('prognosis', axis=1)

y_train = np.array(train['prognosis'])
y_test = np.array(test['prognosis'])

# %% [code]
y_train.shape

# %% [code]
y_test.shape

# %% [code]
X_train.shape

# %% [code]
X_test.shape

# %% [code]
y_train_enc = pd.get_dummies(y_train)
y_train_enc

# %% [code]
y_train_enc.shape

# %% [code]
y_test_enc = pd.get_dummies(y_test)

# %% [code]
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import EarlyStopping

# %% [code]
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(y_train_enc.shape[1], activation='softmax'))

# %% [code]
model.summary()

# %% [code]
model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])

# %% [code]
early_stopping_monitor = EarlyStopping(patience=2, monitor='val_accuracy')
model.fit(X_train, y_train_enc, batch_size=120, epochs=30, validation_split=0.3, callbacks=[early_stopping_monitor])

# %% [code]
model.evaluate(X_test, y_test_enc, batch_size=1, steps=5)

# %% [code]
prediction = model.predict_classes(X_test)

# %% [code]
prediction

# %% [code]
Xnew = train.drop('prognosis', axis=1)
ynew = train['prognosis']

# %% [code]
ynew

# %% [code]
from keras.optimizers import Adam


def create_model(learning_rate, activation):
    model2 = Sequential()
    my_opt = Adam(lr=learning_rate)
    model2.add(Dense(64, activation=activation, input_shape=(X_train.shape[1],)))

    model2.add(Dense(y_train_enc.shape[1], activation='softmax'))
    model2.compile(optimizer=my_opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model2


# %% [code]
from keras.wrappers.scikit_learn import KerasClassifier

modelnew = KerasClassifier(build_fn=create_model, epochs=30, batch_size=100, validation_split=0.3)

# %% [code]
from sklearn.model_selection import RandomizedSearchCV

params = {'activation': ['relu', 'tanh'], 'batch_size': [32, 128, 256],
          'epochs': [10], 'learning_rate': [0.1, 0.01, 0.001]}

random_search = RandomizedSearchCV(modelnew, param_distributions=params, cv=5)
random_search.fit(Xnew, ynew)

# %% [code]
random_search.best_estimator_.fit(Xnew, ynew)

# %% [code]
Xtestnew = test.drop('prognosis', axis=1)
ytestnew = test['prognosis']

# %% [code]
random_search.best_estimator_.score(Xtestnew, ytestnew)

# %% [code]
pred = random_search.best_estimator_.predict(X_test)
pred

# %% [raw]
#