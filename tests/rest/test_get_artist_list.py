import json
import mock

import pytest
from flask import Response

from wgp_demo.pypline import response_object as res


@pytest.fixture
def not_empty_artist_list():
    artists = [
        {
            'uuid': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
            'gender': 'F',
            'age': 39,
            'longitude': '-0.09998975',
            'latitude': '51.75436293',
            'rate': 14.21
        },
        {
            'uuid': 'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
            'gender': 'M',
            'age': 66,
            'longitude': '0.18228006',
            'latitude': '51.74640997',
            'rate': 39.5
        },
        {
            'uuid': '913694c6-435a-4366-ba0d-da5334a611b2',
            'gender': 'M',
            'age': 60,
            'longitude': '0.27891577',
            'latitude': '51.45994069',
            'rate': 27.77
        },
        {
            'uuid': 'eed76e77-55c1-41ce-985d-ca49bf6c0585',
            'gender': 'M',
            'age': 48,
            'longitude': '0.33894476',
            'latitude': '51.39916678',
            'rate': 30.44
        }
    ]

    return artists


@pytest.fixture
def empty_response_object():
    return res.ResponseSuccess([])


@pytest.fixture
def not_empty_response_object(not_empty_artist_list):
    return res.ResponseSuccess(not_empty_artist_list)


def test_use_case_correctly_initialized(client, not_empty_response_object):
    with mock.patch('wgp_demo.repositories.artist_json_repository.ArtistJsonRepository') as mock_repo:
        with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
            mock_use_case().execute.return_value = not_empty_response_object
            client.get('/artists')

        mock_use_case.assert_called_with(mock_repo())


def test_artist_list(client, not_empty_response_object):
    with mock.patch('wgp_demo.pypline.http_response.HttpResponse') as mock_http_response:
        mock_http_response().json.return_value = Response(json.dumps(not_empty_response_object.value),
                                                          mimetype='application/json',
                                                          status=200)
        with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
            mock_use_case().execute.return_value = not_empty_response_object
            response = client.get('/artists')

    mock_http_response.assert_called_with(not_empty_response_object)
    assert mock_http_response().json.called

    assert response.status_code == 200


def test_empty_artist_list(client, empty_response_object):
    with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
        mock_use_case().execute.return_value = empty_response_object

        response = client.get('/artists')

    assert response.status_code == 200
    assert json.loads(response.data.decode('UTF-8')) == []


def test_request_object_initialisation_and_use_without_parameters(client, empty_response_object):
    internal_request_object = mock.Mock()

    with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
        mock_use_case().execute.return_value = empty_response_object
        with mock.patch('wgp_demo.use_cases.request_object.ArtistListRequestObject') as mock_request_object:
            mock_request_object.from_dict.return_value = internal_request_object
            client.get('/artists')

    mock_request_object.from_dict.assert_called_with({'filters': {}, 'rankings': {}})
    mock_use_case().execute.assert_called_with(internal_request_object)


def test_request_object_initialisation_and_use_with_filters(client, empty_response_object):
    internal_request_object = mock.Mock()

    with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
        mock_use_case().execute.return_value = empty_response_object
        with mock.patch('wgp_demo.use_cases.request_object.ArtistListRequestObject') as mock_request_object:
            mock_request_object.from_dict.return_value = internal_request_object
            client.get('/artists?filter_param1=value1&filter_param2=value2')

    mock_request_object.from_dict.assert_called_with(
        {'filters': {'param1': 'value1', 'param2': 'value2'}, 'rankings': {}})
    mock_use_case().execute.assert_called_with(internal_request_object)


def test_request_object_initialisation_and_use_with_rankings(client, empty_response_object):
    internal_request_object = mock.Mock()

    with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
        mock_use_case().execute.return_value = empty_response_object
        with mock.patch('wgp_demo.use_cases.request_object.ArtistListRequestObject') as mock_request_object:
            mock_request_object.from_dict.return_value = internal_request_object
            client.get('/artists?ranking_param1=value1&ranking_param2=value2')

    mock_request_object.from_dict.assert_called_with(
        {'rankings': {'param1': 'value1', 'param2': 'value2'}, 'filters': {}})
    mock_use_case().execute.assert_called_with(internal_request_object)


def test_request_object_initialisation_and_use_with_filters_andrankings(client, empty_response_object):
    internal_request_object = mock.Mock()

    with mock.patch('wgp_demo.use_cases.artist_use_cases.ArtistListUseCase') as mock_use_case:
        mock_use_case().execute.return_value = empty_response_object
        with mock.patch('wgp_demo.use_cases.request_object.ArtistListRequestObject') as mock_request_object:
            mock_request_object.from_dict.return_value = internal_request_object
            client.get('/artists?filter_param1=value1&filter_param2=value2&ranking_param1=value3&ranking_param2=value4')

    mock_request_object.from_dict.assert_called_with({
        'filters': {'param1': 'value1', 'param2': 'value2'},
        'rankings': {'param1': 'value3', 'param2': 'value4'}
    })
    mock_use_case().execute.assert_called_with(internal_request_object)
