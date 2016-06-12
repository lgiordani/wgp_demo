import json

from geopy.distance import great_circle

from wgp_demo.domain import models as domod


class ArtistJsonRepository(object):
    def __init__(self, filepath):
        with open(filepath) as f:
            data = f.read()

        self.data = json.loads(data)
        self.ranks = ['age', 'distance', 'rate']

    def _compute_distance(self, artist, latlon):
        artist_latlon = (artist.latitude, artist.longitude)

        return great_circle(artist_latlon, latlon).miles

    def _normalize_data(self, data):
        if None in data or len(data) == 0:
            return data

        min_data = min(data)
        max_data = max(data)

        norm = max_data - min_data
        if norm == 0:
            return [1] * len(data)

        return [(d - min_data) / norm for d in data]

    def _normalize_artist_ranks(self, artist_list):
        normalized_datasets = []

        for rank in self.ranks:
            attr = rank + '_rank'
            normalized_datasets.append(self._normalize_data([getattr(artist, attr) for artist in artist_list]))

        for artist, age_rank, distance_rank, rate_rank in zip(artist_list, *normalized_datasets):
            artist.age_rank = age_rank
            artist.distance_rank = distance_rank
            artist.rate_rank = rate_rank

    def _filter_by_age(self, _filters, artist_list):
        if 'age' not in _filters:
            return artist_list

        try:
            age_min_str, age_max_str = _filters['age'].split(',')
        except ValueError:
            age_min_str = age_max_str = _filters['age']

        age_min = int(age_min_str)
        age_max = int(age_max_str)
        avg_age = age_min + float(age_max - age_min) / 2

        _artist_list = []
        for artist in artist_list:
            if age_max >= artist.age >= age_min:
                artist.age_rank = avg_age - abs(artist.age - avg_age)
                _artist_list.append(artist)

        return _artist_list

    def _filter_by_distance(self, _filters, artist_list):
        if 'location' in _filters:
            latitude, longitude, radius = _filters['location'].split(',')

            latlon = (float(latitude), float(longitude))
            radius = float(radius)

            _artist_list = []
            for artist in artist_list:
                distance = self._compute_distance(artist, latlon)

                if distance < radius:
                    if distance == 0:
                        distance += 10e-5
                    artist.distance_rank = 1 / distance
                    artist.distance = distance
                    _artist_list.append(artist)

            artist_list = _artist_list

        return artist_list

    def _filter_by_rate(self, _filters, artist_list):
        if 'rate_max' in _filters:
            _artist_list = []
            for artist in artist_list:
                if artist.rate <= float(_filters['rate_max']):
                    artist.rate_rank = abs(float(_filters['rate_max']) - artist.rate)
                    _artist_list.append(artist)

            artist_list = _artist_list

        return artist_list

    def _filter_by_gender(self, _filters, artist_list):
        if 'gender' in _filters:
            artist_list = [artist for artist in artist_list if artist.gender == _filters['gender']]

        return artist_list

    def _compute_global_rank(self, artist, weights_dict):
        weighted_ranks = []

        for rank in self.ranks:
            artist_rank = getattr(artist, rank + "_rank")
            weighted_ranks.append(artist_rank * weights_dict[rank])

        artist.global_rank = sum(weighted_ranks)

    def _order_by_rank(self, weights_dict, artist_list):
        for artist in artist_list:
            self._compute_global_rank(artist, weights_dict)

        global_ranks = [artist.global_rank for artist in artist_list]
        normalized_global_ranks = self._normalize_data(global_ranks)

        for artist, normalized_global_rank in zip(artist_list, normalized_global_ranks):
            artist.global_rank = normalized_global_rank

        sorted_artists_by_global_rank = sorted(artist_list, key=lambda x: x.global_rank, reverse=True)

        return sorted_artists_by_global_rank

    def list(self, filters=None, weights=None):
        if filters is not None:
            _filters = filters
        else:
            _filters = {}

        if weights is not None:
            _weights = weights
        else:
            _weights = {}

        self._normalize_weights(_weights)

        artist_list = [domod.Artist.from_dict(artist) for artist in self.data['artists']]
        artist_list = self._filter_by_age(_filters, artist_list)
        artist_list = self._filter_by_distance(_filters, artist_list)
        artist_list = self._filter_by_rate(_filters, artist_list)
        artist_list = self._filter_by_gender(_filters, artist_list)

        self._normalize_artist_ranks(artist_list)

        artist_list = self._order_by_rank(_weights, artist_list)

        return artist_list

    def _normalize_weights(self, _weights):
        for key, value in _weights.items():
            _weights[key] = float(value)

        for rank in self.ranks:
            if rank not in _weights:
                _weights[rank] = 0

        norm = sum(_weights.values())
        if norm == 0:
            for rank in self.ranks:
                _weights[rank] = 1
