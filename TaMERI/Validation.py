#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
from sklearn.model_selection import cross_validate
#TaMERI libraries/scripts
import NeuralNetwork as TaMERI_NN

#-----------------------------------------------------#
#                 Validation functions                #
#-----------------------------------------------------#
def cross_validation(set_x, set_y):
    neural_network = TaMERI_NN.create_NeuralNetwork()
    #print(set_x)
    #TODO: Eigene cross validation implementieren, um die Ergebnisse zu speichern/zu plotten
    scores = cross_validate(neural_network, set_x, set_y, scoring=['neg_mean_absolute_error'], cv=5, return_train_score=True)
    print(scores)
#
# from sklearn.metrics import recall_score
#
# scoring = ['precision_macro', 'recall_macro']
# clf = svm.SVC(kernel='linear', C=1, random_state=0)
# scores = cross_validate(clf, iris.data, iris.target, scoring=scoring,
#                         cv=5, return_train_score=False)
# sorted(scores.keys())






#NN.train_model(x_train, y_train, (6,6), 1000)
#
# #use trained neural network to predict test data set
# predictions = NN.predict(x_test)
#
# #evaluate predictions
# real = y_test.tolist()
# for i, pred in enumerate(predictions):
#     print(str(pred) + "\t" + str(real[i]) + "\t" + str(pred-real[i]))
#
# # #evaluate predictions
# # #print(confusion_matrix(y_test,predictions))
# # #print(classification_report(y_test,predictions))
#
# from sklearn.model_selection import train_test_split
#
# def split_data(x, y):
# #split data
# x_train, x_test, y_train, y_test = train_test_split(x, y)
# return x_train, x_test, y_train, y_test
