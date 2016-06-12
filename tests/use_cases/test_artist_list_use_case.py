import mock
import pytest

from wgp_demo.domain import models as domod
from wgp_demo.use_cases import request_object as ro
from wgp_demo.use_cases import artist_use_cases as suc


@pytest.fixture
def domain_artists():
    artist_1 = domod.Artist(
        uuid='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        gender='F',
        age=39,
        longitude='-0.09998975',
        latitude='51.75436293',
        rate=14.21,
    )

    artist_2 = domod.Artist(
        uuid='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
        gender='M',
        age=66,
        longitude='0.18228006',
        latitude='51.74640997',
        rate=39.5,
    )

    artist_3 = domod.Artist(
        uuid='913694c6-435a-4366-ba0d-da5334a611b2',
        gender='M',
        age=60,
        longitude='0.27891577',
        latitude='51.45994069',
        rate=27.77,
    )

    artist_4 = domod.Artist(
        uuid='eed76e77-55c1-41ce-985d-ca49bf6c0585',
        gender='M',
        age=48,
        longitude='0.33894476',
        latitude='51.39916678',
        rate=30.44,
    )

    return [artist_1, artist_2, artist_3, artist_4]


def test_artist_list_without_parameters(domain_artists):
    artist_repo = mock.Mock()
    artist_repo.list.return_value = domain_artists

    artist_list_use_case = suc.ArtistListUseCase(artist_repo)
    request_object = ro.ArtistListRequestObject.from_dict({})

    response_object = artist_list_use_case.execute(request_object)

    assert bool(response_object) is True
    artist_repo.list.assert_called_with(filters=None, weights=None)

    assert response_object.value == domain_artists


def test_artist_list_with_filters(domain_artists):
    artist_repo = mock.Mock()
    artist_repo.list.return_value = domain_artists

    artist_list_use_case = suc.ArtistListUseCase(artist_repo)
    qry_filters = {'a': 5}
    request_object = ro.ArtistListRequestObject.from_dict({'filters': qry_filters})

    response_object = artist_list_use_case.execute(request_object)

    assert bool(response_object) is True
    artist_repo.list.assert_called_with(filters=qry_filters, weights=None)
    assert response_object.value == domain_artists


def test_artist_list_with_weights(domain_artists):
    artist_repo = mock.Mock()
    artist_repo.list.return_value = domain_artists

    artist_list_use_case = suc.ArtistListUseCase(artist_repo)
    qry_weights = {'a': 5}
    request_object = ro.ArtistListRequestObject.from_dict({'weights': qry_weights})

    response_object = artist_list_use_case.execute(request_object)

    assert bool(response_object) is True
    artist_repo.list.assert_called_with(filters=None, weights=qry_weights)
    assert response_object.value == domain_artists


def test_artist_list_with_filters_and_weights(domain_artists):
    artist_repo = mock.Mock()
    artist_repo.list.return_value = domain_artists

    artist_list_use_case = suc.ArtistListUseCase(artist_repo)
    qry_filters = {'f': 6}
    qry_weights = {'r': 5}
    request_object = ro.ArtistListRequestObject.from_dict(
        {
            'filters': qry_filters,
            'weights': qry_weights
        }
    )

    response_object = artist_list_use_case.execute(request_object)

    assert bool(response_object) is True
    artist_repo.list.assert_called_with(filters=qry_filters, weights=qry_weights)
    assert response_object.value == domain_artists


def test_artist_list_handles_generic_error():
    artist_repo = mock.Mock()
    artist_repo.list.side_effect = Exception

    artist_list_use_case = suc.ArtistListUseCase(artist_repo)
    request_object = ro.ArtistListRequestObject.from_dict({})

    response_object = artist_list_use_case.execute(request_object)

    assert bool(response_object) is False
