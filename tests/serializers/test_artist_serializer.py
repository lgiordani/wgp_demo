import json

from wgp_demo.serializers import artist_serializer as asr
from wgp_demo.domain import models as domod


def test_serialize_domain_artist_without_rankings():
    artist = domod.Artist('f853578c-fc0f-4e65-81b8-566c5dffa35a', gender='F', age=39, longitude='-0.09998975',
                          latitude='51.75436293', rate=14.21)

    expected_json = """
        {
            "uuid": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "gender": "F",
            "age": 39,
            "longitude": -0.09998975,
            "latitude": 51.75436293,
            "rate": 14.21,
            "distance": null,
            "distance_rank": 0,
            "age_rank": 0,
            "rate_rank": 0,
            "global_rank": null
        }
    """

    assert json.loads(json.dumps(artist, cls=asr.ArtistEncoder)) == json.loads(expected_json)

def test_serialize_domain_artist_with_rankings():
    artist = domod.Artist('f853578c-fc0f-4e65-81b8-566c5dffa35a', gender='F', age=39, longitude='-0.09998975',
                          latitude='51.75436293', rate=14.21)

    artist.distance = 1
    artist.age_rank = 2
    artist.distance_rank = 3
    artist.rate_rank = 4
    artist.global_rank = 5

    expected_json = """
        {
            "uuid": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "gender": "F",
            "age": 39,
            "longitude": -0.09998975,
            "latitude": 51.75436293,
            "rate": 14.21,
            "distance": 1,
            "distance_rank": 3,
            "age_rank": 2,
            "rate_rank": 4,
            "global_rank": 5
        }
    """

    assert json.loads(json.dumps(artist, cls=asr.ArtistEncoder)) == json.loads(expected_json)
