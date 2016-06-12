import json


class ArtistEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'uuid': o.uuid,
                "gender": o.gender,
                "age": o.age,
                "latitude": o.latitude,
                "longitude": o.longitude,
                "rate": o.rate,
                "distance": o.distance,
                "distance_rank": o.distance_rank,
                "age_rank": o.age_rank,
                "rate_rank": o.rate_rank,
                "global_rank": o.global_rank
            }
            return to_serialize
        except AttributeError:
            return super(ArtistEncoder, self).default(o)


