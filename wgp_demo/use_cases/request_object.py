from wgp_demo.shared import request_object as plro


class ArtistListRequestObject(plro.ValidRequestObject):
    def __init__(self, filters=None, weights=None):
        self.filters = filters
        self.weights = weights

    @classmethod
    def from_dict(cls, adict):
        return ArtistListRequestObject(
            filters=adict.get('filters', None),
            weights=adict.get('weights', None)
        )
