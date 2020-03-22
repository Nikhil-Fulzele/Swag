# Swag

A simple wrapper around ml-model tools to track the parameters, training time and metrics.

Planned Support: 
1. sklearn (WIP)
2. keras (TODO)
3. tensorflow (TODO)
4. xgboost (WIP)
5. LGBM (TODO)

The output is stored in SQLite by default.

## Setup and installation
1. Install Python 3.7+
2. Install the package from develop branch - 
```bash
pip install git+https://github.com/Nikhil-Fulzele/Swag.git@develop
```

## Usage 
```python

# Import Ml-libraries
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn import datasets
from random import randint

# Import Swag
from swag import Swag

# Initialize with Experiment Name - mandatory
s = Swag("Exp Name") 
swag = s.swag # NOTE: do not put round brackets after swag 

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
    swag(nn.fit)(X, y) # NOTE: Carefully wrap only the fit method and not the parameters

    # Measure with swag
    swag(mean_squared_error)(y, nn.predict(X))

    # Measure with swag
    swag(r2_score)(y, nn.predict(X))

    # Measure with swag
    yhat = nn.predict(X)
    swag(mean_absolute_error)(y, yhat)

s.get_json() # to display the output in pretty dict format

```
Refer example folder for more working examples.