import googlemaps


class GPSAddressConverter:
    def __init__(self):
        self.gmaps = googlemaps.Client(key='AIzaSyD93yCYLOXT1i73lWnz00ULpyacHArBEcQ')

    def convert(self, address):
        return self.gmaps.geocode(address)[0]['geometry']['location']

