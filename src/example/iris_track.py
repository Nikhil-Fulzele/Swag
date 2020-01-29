from sklearn.neural_network import MLPRegressor
from sklearn import datasets

from src.swag import Swag

if __name__ == '__main__':

    # Initialize
    s = Swag("Exp_name")
    swag = s.swag

    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Initialize model
    nn = MLPRegressor(hidden_layer_sizes=(10, 2, ), n_iter_no_change=10, activation="tanh", max_iter=10)

    # Fit with swag
    swag(nn.fit)(X, y)

    # Predict swag
    swag(nn.predict)(X)

    s.show()

