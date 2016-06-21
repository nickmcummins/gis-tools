import googlemaps


class GPSAddressConverter:
    def __init__(self):
        self.gmaps = googlemaps.Client(key='')

    def convert(self, address):
        return self.gmaps.geocode(address)[0]['geometry']['location']

