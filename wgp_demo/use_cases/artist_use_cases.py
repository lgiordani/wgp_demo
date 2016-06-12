from wgp_demo.pypline import response_object as ro
from wgp_demo.pypline import use_case as uc


class ArtistListUseCase(uc.UseCase):
    def __init__(self, artist_repo):
        self.artist_repo = artist_repo

    def process_request(self, request_object):
        domain_artists = self.artist_repo.list(
            filters=request_object.filters,
            rankings=request_object.rankings
        )
        return ro.ResponseSuccess(domain_artists)