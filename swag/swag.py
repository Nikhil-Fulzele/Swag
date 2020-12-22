from .base_swag import BaseSwag


class Swag(BaseSwag):
    def __init__(self, *args, **kwargs):
        from swag.wrappers.sklearn import fit_wrapper
        fit_wrapper(self)
        super().__init__(*args, **kwargs)
