import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, RandomForestClassifier
from sklearn.svm import SVC

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

#
# def Decision_Tree():
#     tree = DecisionTreeClassifier()
#     tree.fit(x_train, y_train)
#
#     acc = tree.score(x_test, y_test)
#
#     print("Decision Tree Acurray on test set: {:.2f}%".format(acc * 100))
#     # print(tree.get_depth())
#     return tree
#
# ####################################
# def Random_Forest():
#     clf = RandomForestClassifier()
#     clf.fit(x_train, y_train)
#     accForest = clf.score(x_test, y_test)
#     print("Random ForestAcurray on test set: {:.2f}%".format(accForest * 100))
#     return clf
#
# ##############################
#
# # Define Gradient Boosting Classifier with hyperparameters
# def GBC():
#     gbc = GradientBoostingClassifier()
#     gbc.fit(x_train, y_train)
#     # Confusion matrix will give number of correct and incorrect classifications
#     # print(confusion_matrix(y_test, gbc.predict(x_test)))
#     # Accuracy of model
#     print("GBC accuracy is %2.2f", accuracy_score(y_test, gbc.predict(x_test)) * 100)
#     return gbc
#
# #######################################
#
#
# def modelling():
#     #x = df1.drop('prognosis', axis=1).values
#     #y = df1.prognosis
#     #x_train_new, x_test_new, y_train_new, y_test_new = train_test_split(x_new, y_new, test_size=0.3, random_state=42)
#     tree = Random_Forest()
#     #tree.fit(x, y)
#     return tree
# #     pred_new = tree.predict(x_test_new)
# #
# #     acc_new = tree.score(x_test_new, y_test_new)
# #     #     a = mean_absolute_error(y_test_new, pred_new)
# #     print("Acurray on test set: {:.2f}%".format(acc * 100))
# # #   print("mean_absolute_error of the test set: {:.2f}%".format(a))
#
#
# model = modelling()
#
# def predict(symptoms):
#     newTest = np.zeros((1, 132))
#     for symptom in symptoms:
#         # print(symptom)
#         colIndex = x_train.columns.get_loc(symptom)
#         print(symptom , colIndex)
#         newTest[0][colIndex] = 1
#     predict_new_test = model.predict(newTest)
#     return predict_new_test


class Decision_Tree:
    def __init__(self):
        df = pd.read_csv('kaggle/Training.csv')
        # df.describe()
        df.shape
        df.drop('Unnamed: 133', axis=1, inplace=True)
        #self.__df.columns
        # """ prognosis means our labels in data """
        df['prognosis'].value_counts()
        x= df.drop('prognosis', axis=1)
        y = df['prognosis']
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(x, y, test_size=0.7, shuffle=True)

        self.__clf = RandomForestClassifier()
        self._train_model()

    def _train_model(self):
        self.__clf.fit(self.__x_train, self.__y_train)
        accForest = self.__clf.score(self.__x_test, self.__y_test)
        print("Random ForestAcurray on test set: {:.2f}%".format(accForest * 100))

    def predict(self, symptoms):
        newTest = np.zeros((1, 132))
        for symptom in symptoms:
            # print(symptom)
            colIndex = self.__x_train.columns.get_loc(symptom)
            print(symptom, colIndex)
            newTest[0][colIndex] = 1
        predict_new_test = self.__clf.predict(newTest)
        return predict_new_test

#listt = ["red_spots_over_body","headache"]