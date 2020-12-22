from swag.utils import gorilla
from sklearn.utils import all_estimators


def fit_wrapper(swag):

    _estimator_mapper = {}

    for estimator_name, estimator_base_class in all_estimators():
        if not hasattr(estimator_base_class, 'fit'):
            continue

        _estimator_mapper[estimator_name] = estimator_base_class

        def patch_fit(self, *args, **kwargs):
            obj = gorilla.get_original_attribute(_estimator_mapper[self.__class__.__name__], 'fit')
            swag.swag(self, obj, "run_name")
            obj(self, *args, **kwargs)
            return self

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        patch = gorilla.Patch(estimator_base_class, 'fit', patch_fit, settings=settings)
        gorilla.apply(patch)
