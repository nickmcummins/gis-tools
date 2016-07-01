from lxml import etree
from gpxpy.gpx import GPX, GPXTrackPoint
from gps.gps_address_converter import GPSAddressConverter


class StreetAddress:
    def __init__(self, address_string):
        self.address_converter = GPSAddressConverter()
        self.address_string = address_string

    def to_gps_coordinates(self):
        return self.address_converter.convert(self.address_string)

    def to_gpx(self):
        gpx = GPX()
        gps = self.to_gps_coordinates()
        gpx.waypoints.append(GPXTrackPoint(gps['lat'], gps['lng']))
        gpx_xml = gpx.to_xml()
        return etree.tostring(etree.fromstring(gpx_xml.encode('utf-8'), parser=etree.XMLParser(encoding='utf-8')),
                              pretty_print=True).decode('utf-8')
