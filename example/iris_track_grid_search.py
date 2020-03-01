from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import datasets
from sklearn import svm
from swag import Swag

if __name__ == '__main__':

    # Initialize
    exp_name = "Iris Exp - Grid"
    s = Swag(exp_name)
    swag = s.swag

    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Initialize model
    parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
    svc = svm.SVC()
    clf = GridSearchCV(svc, parameters)

    # Fit with swag
    swag(clf.fit)(X, y)

    # Measure with swag
    swag(mean_squared_error)(y, clf.predict(X))

    # Measure with swag
    swag(r2_score)(y, clf.predict(X))

    # Measure with swag
    yhat = clf.predict(X)
    swag(mean_absolute_error)(y, yhat)

    s.visualize_experiment(experiment_name=exp_name)

    s.visualize_experiment(experiment_name=exp_name, kind='params')
