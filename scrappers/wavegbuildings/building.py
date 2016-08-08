from gpxpy.gpx import GPXTrackPoint


class Building:
    def __init__(self, name, address, speeds, geocoder):
        self.name = name
        self.address = address
        self.internet = speeds
        self.geocoder = geocoder

    @staticmethod
    def from_tag(html_tag, geocoder):
        name = html_tag.find("a", {"class": "bldg_title"}).text
        address, speeds, *_ = html_tag.p.text.split('\n')
        return Building(name, address, speeds, geocoder)

    def __repr__(self):
        return self.name + "\n" + self.address + '\n'

    def to_gpx_trackpoint(self):
        gps = self.geocoder.convert(self.address)
        trackpoint = GPXTrackPoint(gps['lat'], gps['lng'])
        trackpoint.name = self.name
        return trackpoint
