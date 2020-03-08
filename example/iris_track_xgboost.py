from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import datasets
from swag import Swag

if __name__ == '__main__':

    # Initialize
    exp_name = "Iris Experiment - XGBOOST"
    s = Swag(exp_name)
    swag = s.swag

    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Initialize model
    nn = XGBRegressor(n_estimators=15, n_jobs=-1)

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

    s.visualize_experiment(experiment_name=exp_name)
