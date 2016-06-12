import pytest

from wgp_demo.use_cases import request_object as ro


def test_build_site_list_request_object_without_parameters():
    req = ro.ArtistListRequestObject()

    assert req.filters is None
    assert bool(req) is True


def test_build_site_list_request_object_with_empty_filters():
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


def test_build_site_list_request_object_with_empty_rankings():
    req = ro.ArtistListRequestObject(rankings={})

    assert req.rankings == {}
    assert bool(req) is True


def test_build_file_list_request_object_from_dict_with_empty_rankings():
    req = ro.ArtistListRequestObject.from_dict({'rankings': {}})

    assert req.rankings == {}
    assert bool(req) is True


def test_build_file_list_request_object_from_dict_with_rankings():
    req = ro.ArtistListRequestObject.from_dict({'rankings': {'a': 2, 'b': 3}})

    assert req.rankings == {'a': 2, 'b': 3}
    assert bool(req) is True
