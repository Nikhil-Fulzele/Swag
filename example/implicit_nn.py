# Import Ml-libraries
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import datasets
from random import randint
from random import choices

# Import Swag
from swag import Swag

if __name__ == '__main__':
    # Initialize with Experiment Name - mandatory
    exp_name = "Experiment-2"
    swag = Swag(exp_name)

    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    for i in range(30):

        a = randint(1, 5)
        b = randint(1, 10)
        activation = choices(['identity', 'logistic', 'tanh', 'relu'])[0]
        max_iter = randint(5, 10)

        # Initialize model
        nn = MLPRegressor(hidden_layer_sizes=(a, b, ), activation=activation, max_iter=max_iter)

        nn.fit(X, y)

        mean_squared_error(y, nn.predict(X))

        r2_score(y, nn.predict(X))

        yhat = nn.predict(X)
        mean_absolute_error(y, yhat)

    swag.visualize_experiment(experiment_name=exp_name)
