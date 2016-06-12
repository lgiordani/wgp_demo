import pytest

from wgp_demo.use_cases import request_object as ro


def test_build_artist_list_request_object_without_parameters():
    req = ro.ArtistListRequestObject()

    assert req.filters is None
    assert bool(req) is True


def test_build_artist_list_request_object_with_empty_filters():
    req = ro.ArtistListRequestObject(filters={})

    assert req.filters == {}
    assert bool(req) is True


def test_build_file_list_request_object_from_dict_with_empty_filters():
    req = ro.ArtistListRequestObject.from_dict({'filters': {}})

    assert req.filters == {}
    assert bool(req) is True


def test_build_file_list_request_object_from_dict_with_filters():
    req = ro.ArtistListRequestObject.from_dict({'filters': {'a': 2, 'b': 3}})

    assert req.filters == {'a': 2, 'b': 3}
    assert bool(req) is True


def test_build_artist_list_request_object_with_empty_weights():
    req = ro.ArtistListRequestObject(weights={})

    assert req.weights == {}
    assert bool(req) is True


def test_build_file_list_request_object_from_dict_with_empty_weights():
    req = ro.ArtistListRequestObject.from_dict({'weights': {}})

    assert req.weights == {}
    assert bool(req) is True


def test_build_file_list_request_object_from_dict_with_weights():
    req = ro.ArtistListRequestObject.from_dict({'weights': {'a': 2, 'b': 3}})

    assert req.weights == {'a': 2, 'b': 3}
    assert bool(req) is True
