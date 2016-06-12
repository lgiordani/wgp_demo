from wgp_demo.domain import models as m


def test_artist_model_init():
    artist = m.Artist('f853578c-fc0f-4e65-81b8-566c5dffa35a', gender='F', age=39, longitude='-0.09998975',
                      latitude='51.75436293', rate=14.21)
    assert artist.uuid == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    assert artist.gender == 'F'
    assert artist.age == 39
    assert artist.longitude == -0.09998975
    assert artist.latitude == 51.75436293
    assert artist.rate == 14.21
    assert artist.distance_rank == None
    assert artist.age_rank == None
    assert artist.rate_rank == None
    assert artist.global_rank == None


def test_artist_model_from_dict():
    artist = m.Artist.from_dict(
        {
            'uuid': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
            'gender': 'F',
            'age': 39,
            'longitude': '-0.09998975',
            'latitude': '51.75436293',
            'rate': 14.21
        }
    )

    assert artist.uuid == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    assert artist.gender == 'F'
    assert artist.age == 39
    assert artist.longitude == -0.09998975
    assert artist.latitude == 51.75436293
    assert artist.rate == 14.21
    assert artist.distance_rank == None
    assert artist.age_rank == None
    assert artist.rate_rank == None
    assert artist.global_rank == None
