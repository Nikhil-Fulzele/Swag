from sklearn.model_selection import GridSearchCV
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

    # s.show()

    s.visualize_experiment(experiment_name=exp_name)

    s.visualize_experiment(experiment_name=exp_name, kind='params')