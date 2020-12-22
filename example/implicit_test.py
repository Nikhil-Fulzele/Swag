from random import randint
import numpy as np

from sklearn.neural_network import MLPRegressor
from sklearn.mixture import GaussianMixture
from sklearn import svm

from swag import Swag

if __name__ == '__main__':
    exp_name = "Experiment-1"
    swag = Swag(exp_name)

    X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0], [14, 12]])
    y = np.array([1, 2, 3, 4, 5, 6, 7])

    gm = GaussianMixture(n_components=2, random_state=10)
    gm.fit(X, y)

    a = randint(1, 5)
    b = randint(1, 10)
    nn = MLPRegressor(hidden_layer_sizes=(a, b,), n_iter_no_change=10, activation="tanh", max_iter=10)
    nn.fit(X, y)

    svc = svm.SVC(degree=5)
    svc.fit(X, y)

    swag.visualize_experiment(experiment_name=exp_name)
