from sklearn.model_selection import GridSearchCV
from sklearn import datasets
from sklearn import svm

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
    parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
    svc = svm.SVC()
    clf = GridSearchCV(svc, parameters)
    clf.fit(iris.data, iris.target)

    # Fit with swag
    swag(clf.fit)(X, y)

    s.show()
