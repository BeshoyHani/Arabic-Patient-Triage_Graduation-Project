import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
from sklearn.svm import SVC

df = pd.read_csv('kaggle/Training.csv')
df_test = pd.read_csv("kaggle/Testing.csv")
#
# df.describe()

df.shape

df.drop('Unnamed: 133', axis=1, inplace=True)
df.columns

# """ prognosis means our labels in data """

df['prognosis'].value_counts()

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import mean_absolute_error

tree = DecisionTreeClassifier()

from sklearn.model_selection import train_test_split

x = df.drop('prognosis', axis=1)
y = df['prognosis']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=True, random_state=42)
tree.fit(x_train, y_train)

pred = tree.predict(x_test)
acc = tree.score(x_test, y_test)

print("Acurray on test set: {:.2f}%".format(acc * 100))
# print(tree.get_depth())
################################
####
clf = RandomForestClassifier()
clf.fit(x_train, y_train)
predforest = clf.predict(x_test)
accForest = clf.score(x_test, y_test)
print("Acurray on test set: {:.2f}%".format(accForest * 100))
####
####
# Create adaboost classifer object
# svc=SVC(probability=True, kernel='linear')
# abc = AdaBoostClassifier(base_estimator=svc)
# Train Adaboost Classifer
# modelabd = abc.fit(x_train, y_train)

#Predict the response for test dataset
# y_pred = modelabd.predict(x_test)
# print("Accuracy:",metrics.accuracy_score(y_test, y_pred)*100)
####

#######
# Define Gradient Boosting Classifier with hyperparameters
gbc=GradientBoostingClassifier()
# Fit train data to GBC
gbc.fit(x_train, y_train)
# Confusion matrix will give number of correct and incorrect classifications
#print(confusion_matrix(y_test, gbc.predict(x_test)))

# Accuracy of model
print("GBC accuracy is %2.2f" , accuracy_score(y_test, gbc.predict(x_test))*100)

#######
################################

fi = pd.DataFrame(tree.feature_importances_ * 100, x_test.columns, columns=['Importance'])
fi.sort_values(by='Importance', ascending=False, inplace=True)
fi

zeros = np.array(fi[fi['Importance'] <= 2.300000].index)
zeros

training_new = df.drop(columns=zeros, axis=1)
training_new.shape[1]
training_new.columns


def modelling(df1):
    x = df1.drop('prognosis', axis=1).values
    y = df1.prognosis
    #x_train_new, x_test_new, y_train_new, y_test_new = train_test_split(x_new, y_new, test_size=0.3, random_state=42)
    tree.fit(x, y)
    return tree
#     pred_new = tree.predict(x_test_new)
#
#     acc_new = tree.score(x_test_new, y_test_new)
#     #     a = mean_absolute_error(y_test_new, pred_new)
#     print("Acurray on test set: {:.2f}%".format(acc * 100))
# #   print("mean_absolute_error of the test set: {:.2f}%".format(a))


test = pd.read_csv('kaggle/Testing.csv')
test_new = test.drop(columns=zeros, axis=1)
test_new.shape[1]

model = modelling(test)


def testing(symptoms,mode):
    newTest = np.zeros((1, 132))
    for symptom in symptoms:
        # print(symptom)
        colIndex = x_train.columns.get_loc(symptom)
        print(symptom , colIndex)
        newTest[0][colIndex] = 1
    predict_new_test = mode.predict(newTest)
    return predict_new_test



listt = ["red_spots_over_body","headache"]
print(testing(listt,tree))
print(testing(listt,clf))
print(testing(listt,gbc))
# print(testing(listt,modelabd))