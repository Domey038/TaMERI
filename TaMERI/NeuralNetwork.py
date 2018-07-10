from sklearn.neural_network import MLPRegressor
import pickle

def train_model(training_data, training_result):
    model = MLPRegressor(hidden_layer_sizes=(6,6),max_iter=10000)
    model.fit(training_data, training_result)
    pickle.dump(model, open("data/NN_model.pickle", 'wb'))

def predict(data):
    model = pickle.load(open("data/NN_model.pickle", 'rb'))
    predictions = model.predict(data)
    return predictions
