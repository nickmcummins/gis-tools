from gpxpy.gpx import GPXTrackPoint

from gps.gps_address_converter import GPSAddressConverter


class Building:
    def __init__(self, name, address, speeds):
        self.name = name
        self.address = address
        self.internet = speeds

    @staticmethod
    def from_tag(html_tag):
        name = html_tag.find("a", {"class": "bldg_title"}).text
        address, speeds, *_ = html_tag.p.text.split('\n')
        return Building(name, address, speeds)

    def __repr__(self):
        return self.name + "\n" + self.address + '\n'

    def to_gpx_trackpoint(self):
        gps = GPSAddressConverter().convert(self.address)
        trackpoint = GPXTrackPoint(gps['lat'], gps['lng'])
        trackpoint.name = self.name
        return trackpoint
