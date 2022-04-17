import pandas as pd
import numpy as np
df = pd.read_csv('kaggle/Training.csv')
df_test = pd.read_csv("kaggle/Testing.csv")
#
# df.describe()

df.shape

#df.drop('Unnamed: 133', axis=1, inplace=True)
df.columns

# """ prognosis means our labels in data """

df['prognosis'].value_counts()

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import mean_absolute_error

tree = DecisionTreeClassifier()

from sklearn.model_selection import train_test_split

x_train = df.drop('prognosis', axis=1)
y_train = df['prognosis']

x_test = df_test.drop('prognosis', axis=1)
y_test = df_test['prognosis']

tree.fit(x_train, y_train)

pred = tree.predict(x_test)
acc = tree.score(x_test, y_test)

print("Acurray on test set: {:.2f}%".format(acc * 100))


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


def testing(symptoms):
    newTest = np.zeros((1, 132))
    for symptom in symptoms:
        # print(symptom)
        colIndex = x_train.columns.get_loc(symptom)
        print(symptom , colIndex)
        newTest[0][colIndex] = 1
    predict_new_test = model.predict(newTest)
    return predict_new_test



listt = [ "watering_from_eyes", "chills","continuous_sneezing","continuous_feel_of_urine"]
print(testing(listt))