from wgp_demo.pypline import domain as ppld


class DomainModel(ppld.DomainModel):
    pass


class Artist(object):
    def __init__(self, uuid, gender, age, latitude, longitude, rate):
        self.uuid = uuid
        self.gender = gender
        self.age = age
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.rate = rate
        self.distance_rank = None
        self.age_rank = None
        self.rate_rank = None
        self.global_rank = None

    @classmethod
    def from_dict(cls, adict):
        artist = Artist(
            uuid=adict['uuid'],
            gender=adict['gender'],
            age=adict['age'],
            latitude=adict['latitude'],
            longitude=adict['longitude'],
            rate=adict['rate']
        )

        return artist


DomainModel.register(Artist)
