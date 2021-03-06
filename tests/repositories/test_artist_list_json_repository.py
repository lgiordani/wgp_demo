import os
import pytest
import tempfile
import shutil
import json

from wgp_demo.repositories import artist_json_repository as ajr

from wgp_demo.domain import models as domod

london_position = {
    'latitude': '51.5126064',
    'longitude': '-0.1802461'
}

data_dict = {
    'artists': [
        {
            # Distance from London: 17.059475921200125 miles
            'uuid': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
            'gender': 'F',
            'age': 39,
            'longitude': '-0.09998975',
            'latitude': '51.75436293',
            'rate': 14.21
        },
        {
            # Distance from London: 22.427583701757253 miles
            'uuid': 'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
            'gender': 'M',
            'age': 66,
            'longitude': '0.18228006',
            'latitude': '51.74640997',
            'rate': 39.5
        },
        {
            # Distance from London: 20.093197184470394 miles
            'uuid': '913694c6-435a-4366-ba0d-da5334a611b2',
            'gender': 'M',
            'age': 60,
            'longitude': '0.27891577',
            'latitude': '51.45994069',
            'rate': 27.77
        },
        {
            # Distance from London: 23.69378975969768 miles
            'uuid': 'eed76e77-55c1-41ce-985d-ca49bf6c0585',
            'gender': 'M',
            'age': 48,
            'longitude': '0.33894476',
            'latitude': '51.39916678',
            'rate': 30.44
        }
    ]
}

json_content = json.dumps(data_dict)


@pytest.fixture
def temp_empty_dir(request):
    tempdir = tempfile.mkdtemp()

    def fin():
        shutil.rmtree(tempdir)

    request.addfinalizer(fin)
    return tempdir


@pytest.fixture
def temp_json_file(temp_empty_dir):
    filepath = os.path.join(temp_empty_dir, "artists.json")
    with open(filepath, 'w') as f:
        f.write(json_content)

    return filepath


def test_initialize_repo(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)
    assert len(repo.data) != 0


def test_list_all_artists(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list()

    assert len(artists) == len(data_dict['artists'])
    assert isinstance(artists[0], domod.DomainModel)
    assert set([artist.uuid for artist in artists]) == set([artist['uuid'] for artist in data_dict['artists']])


def test_list_accepts_filters(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={})

    assert len(artists) == len(data_dict['artists'])
    assert isinstance(artists[0], domod.DomainModel)
    assert set([artist.uuid for artist in artists]) == set([artist['uuid'] for artist in data_dict['artists']])


def test_list_discards_unknown_filters(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={'some_unknown_filter': '123'})

    assert len(artists) == len(data_dict['artists'])
    assert isinstance(artists[0], domod.DomainModel)
    assert set([artist.uuid for artist in artists]) == set([artist['uuid'] for artist in data_dict['artists']])


def test_list_can_manage_filtered_data_with_empty_return(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={'age': '120'})

    assert len(artists) == 0


def test_list_can_filter_by_age_with_min_and_max(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={'age': '39,60'})

    assert len(artists) == 3
    assert any([artist.age_rank != 0 for artist in artists])
    assert all([artist.global_rank is not None for artist in artists])


def test_list_can_filter_by_age_with_only_one_value(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={'age': '66'})

    assert len(artists) == 1
    assert any([artist.age_rank != 0 for artist in artists])
    assert all([artist.global_rank is not None for artist in artists])


def test_list_location_filter_format_check(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    with pytest.raises(ValueError):
        repo.list(filters={'location': '51.75436293, -0.09998975'})


def test_list_can_filter_by_location(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(
        filters={'location': '{},{},{}'.format(
            london_position['latitude'],
            london_position['longitude'],
            21.1)
        }
    )

    assert len(artists) == 2
    assert any([artist.distance is not None for artist in artists])
    assert any([artist.distance_rank != 0 for artist in artists])
    assert all([artist.global_rank is not None for artist in artists])


def test_list_filter_by_location_stores_correct_distances(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(
        filters={'location': '{},{},{}'.format(
            london_position['latitude'],
            london_position['longitude'],
            21.1)
        }
    )

    stored_distances = [artist.distance for artist in artists]
    computed_distances = [17.059475921200125, 20.093197184470394]

    for stored_distance, computed_distance in zip(stored_distances, computed_distances):
        assert computed_distance + 1e-4 >= stored_distance >= computed_distance - 1e-4


def test_list_can_filter_by_rate(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(
        filters={'rate_max': '27.1'}
    )

    assert len(artists) == 1
    assert any([artist.rate_rank != 0 for artist in artists])
    assert all([artist.global_rank != 0 for artist in artists])


def test_list_can_filter_by_gender(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(
        filters={'gender': 'F'}
    )

    assert len(artists) == 1


def test_list_with_multiple_filters(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(
        filters={
            'location': '{},{},{}'.format(
                london_position['latitude'],
                london_position['longitude'],
                31.1
            ),
            'gender': 'M',
            'age': '14,50'
        }
    )

    assert len(artists) == 1
    assert all([artist.age_rank == 1 for artist in artists])
    assert all([artist.distance is not None for artist in artists])
    assert all([artist.distance_rank == 1 for artist in artists])
    assert all([artist.rate_rank == 1 for artist in artists])


def test_list_accepts_weights(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={}, weights={})

    assert len(artists) == len(data_dict['artists'])
    assert isinstance(artists[0], domod.DomainModel)
    assert set([artist.uuid for artist in artists]) == set([artist['uuid'] for artist in data_dict['artists']])


def test_list_rank_by_age(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={}, weights={'age': '1'})

    expected_result = [
        'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
        '913694c6-435a-4366-ba0d-da5334a611b2',
        'eed76e77-55c1-41ce-985d-ca49bf6c0585',
    ]

    assert [artist.uuid for artist in artists] == expected_result


def test_list_rank_by_distance(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={
        'location': '{},{},{}'.format(
            london_position['latitude'],
            london_position['longitude'],
            23.1
        ),
    }, weights={'distance': '1'})

    expected_result = [
        'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        '913694c6-435a-4366-ba0d-da5334a611b2',
        'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
    ]

    assert [artist.uuid for artist in artists] == expected_result


def test_list_rank_by_rate(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={'rate_max': '31.1'}, weights={'rate': '1'})
    expected_result = [
        'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        '913694c6-435a-4366-ba0d-da5334a611b2',
        'eed76e77-55c1-41ce-985d-ca49bf6c0585',
    ]

    assert [artist.uuid for artist in artists] == expected_result


def test_list_rank_by_half_distance_half_age(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={
        'location': '{},{},{}'.format(
            london_position['latitude'],
            london_position['longitude'],
            23
        ),
    }, weights={'age': '0.5', 'distance': '0.5'})

    expected_result = [
        'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        '913694c6-435a-4366-ba0d-da5334a611b2',
        'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
    ]

    assert [artist.uuid for artist in artists] == expected_result


def test_list_ranks_shall_be_normalized(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={
        'age': '39,66',
        'location': '{},{},{}'.format(
            london_position['latitude'],
            london_position['longitude'],
            23
        ),
    }, weights={'age': '1', 'distance': '100'})

    expected_result = [
        'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        '913694c6-435a-4366-ba0d-da5334a611b2',
        'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
    ]

    assert [artist.uuid for artist in artists] == expected_result

def test_list_global_ranks_are_normalized(temp_json_file):
    repo = ajr.ArtistJsonRepository(temp_json_file)

    artists = repo.list(filters={
        'age': '39,66',
        'location': '{},{},{}'.format(
            london_position['latitude'],
            london_position['longitude'],
            23
        ),
    }, weights={'age': '1', 'distance': '100'})


    assert all([1 >= artist.global_rank >= 0 for artist in artists])
