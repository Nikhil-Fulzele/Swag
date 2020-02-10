from sklearn.model_selection import RandomizedSearchCV
from sklearn import datasets
from sklearn import svm

from ..swag import Swag

if __name__ == '__main__':

    # Initialize
    s = Swag("Exp_name")
    swag = s.swag

    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Initialize model
    param_distributions = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
    svc = svm.SVC()
    clf = RandomizedSearchCV(svc, param_distributions)

    # Fit with swag
    swag(clf.fit)(X, y)

    s.show()
    s.load()
