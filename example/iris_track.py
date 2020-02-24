from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import datasets
from random import randint
from swag import Swag

if __name__ == '__main__':

    # Initialize
    exp_name = "Iris Experiment3"
    s = Swag(exp_name)
    swag = s.swag

    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    for i in range(3):

        a = randint(1, 5)
        b = randint(1, 10)

        # Initialize model
        nn = MLPRegressor(hidden_layer_sizes=(a, b, ), n_iter_no_change=10, activation="tanh", max_iter=10)

        # Fit with swag
        swag(nn.fit)(X, y)

        # Measure with swag
        swag(mean_squared_error)(y, nn.predict(X))

        # Measure with swag
        swag(r2_score)(y, nn.predict(X))

        # Measure with swag
        yhat = nn.predict(X)
        swag(mean_absolute_error)(y, yhat)

    print(s.get_swag_dataframe(experiment_name=exp_name))

    print(s.get_swag_dataframe(run_id="4af7b124de6546af82a37b642cf9af4a"))

    s.visualize_experiment(experiment_name=exp_name)

    s.visualize_experiment(experiment_name=exp_name, kind='params')
