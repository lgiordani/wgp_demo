from wgp_demo.pypline import request_object as plro


class ArtistListRequestObject(plro.ValidRequestObject):
    def __init__(self, filters=None, rankings=None):
        self.filters = filters
        self.rankings = rankings

    @classmethod
    def from_dict(cls, adict):
        return ArtistListRequestObject(
            filters=adict.get('filters', None),
            rankings=adict.get('rankings', None)
        )
