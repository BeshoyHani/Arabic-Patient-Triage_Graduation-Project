import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings

warnings.filterwarnings('ignore')

train = pd.read_csv('kaggle/Training.csv')
test = pd.read_csv('kaggle/Testing.csv')

# inspecting data
print("Train Shape: ")
print(train.shape)
print("Test Shape: ")
print(test.shape)
# preprocessing Step
train.drop('Unnamed: 133', axis=1, inplace=True)
print("Train shape after dropping unnecessary column: " + str(train.shape))
# More info about the train data
train.info()
train.isna().sum()
train.nunique()

# Dropping thr prognosis column from the features
X_train = train.drop('prognosis', axis=1)
X_test = test.drop('prognosis', axis=1)

# Creating our prognosis "Target" Columns
y_train = np.array(train['prognosis'])
y_test = np.array(test['prognosis'])

# Making a one hot encoding for the output target "Prognosis" Test and Training
y_train_enc = pd.get_dummies(y_train)
print(y_train_enc)
y_test_enc = pd.get_dummies(y_test)

from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import EarlyStopping

'''
Creating our Keras sequential model and adding the necessary
Hidden layers with Activation function 'Relu' and 'Softmax'
Activation function for the output Layer
'''
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(y_train_enc.shape[1], activation='softmax'))

# Printing a summary of the model
print(model.summary())
model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])
early_stopping_monitor = EarlyStopping(patience=2, monitor='val_accuracy')
model.fit(X_train, y_train_enc, batch_size=120, epochs=30, validation_split=0.3, callbacks=[early_stopping_monitor])
model.evaluate(X_test, y_test_enc, steps=5)
prediction = model.predict_classes(X_test)
print(type(X_test))
print(X_test)
print(prediction)


def testing(symptoms):
    newTest = np.zeros((1, 132))
    for symptom in symptoms:
        print(symptom)
        colIndex = X_train.columns.get_loc(symptom)
        newTest[0][colIndex] = 1
    print(y_train_enc.columns.values[(model.predict_classes(newTest))])


listt = ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic _patches"]
testing(listt)
# How we choose our Parameters
"""
"""
Xnew = train.drop('prognosis', axis=1)
ynew = train['prognosis']

from tensorflow.keras.optimizers import Adam


def create_model(learning_rate, activation):
    model2 = Sequential()
    my_opt = Adam(lr=learning_rate)
    model2.add(Dense(64, activation=activation, input_shape=(X_train.shape[1],)))

    model2.add(Dense(y_train_enc.shape[1], activation='softmax'))
    model2.compile(optimizer=my_opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model2

from keras.wrappers.scikit_learn import KerasClassifier
modelnew = KerasClassifier(build_fn=create_model, epochs=30, batch_size=100, validation_split=0.3)

from sklearn.model_selection import RandomizedSearchCV

params = {'activation': ['relu', 'tanh'], 'batch_size': [32, 128, 256],
          'epochs': [10], 'learning_rate': [0.1, 0.01, 0.001]}

random_search = RandomizedSearchCV(modelnew, param_distributions=params, cv=5)
random_search.fit(Xnew, ynew)

random_search.best_estimator_.fit(Xnew, ynew)

Xtestnew = test.drop('prognosis', axis=1)
ytestnew = test['prognosis']

random_search.best_estimator_.score(Xtestnew, ytestnew)
pred = random_search.best_estimator_.predict(X_test)
print(pred)
"""
"""