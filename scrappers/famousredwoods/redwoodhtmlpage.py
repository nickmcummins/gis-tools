import re

from bs4 import BeautifulSoup
from gpxpy.gpx import GPXTrackPoint

GPS_LATITUDE_STRING = "GPS Latitude"
GPS_LATITUDE_RE = r'.*GPS Latitude.*([0-9]{2}\.[0-9]+).*'

GPS_LONGITUDE_STRING = "GPS Longitude"
GPS_LONGITUDE_RE = r'.*GPS Longitude.*(\-[0-9]{3}\.[0-9]+).*'

ELEVATION_STRING = "Elevation:"
ELEVATION_RE = r'.*Elevation.*([0-9]{2})\.?[0-9]*\sm.*'


class RedwoodHTMLPage:
    def __init__(self, html_file):
        self.html_file = BeautifulSoup(open(html_file, encoding='cp1252').read(), 'html.parser')

    def title(self):
        full_title = str(self.html_file.find("title").text)
        return full_title.split(" - ")[0]

    def description(self):
        description = "\n\n".join(list(map(lambda x: x.text.strip(), self.html_file.find_all("table")[3:6]))).strip()
        formatted_description = re.sub(r"\s\s\s+", ' ', description)
        return formatted_description

    def gps_latitude(self):
        gps_latitude_matches = list(
            filter(lambda x: x.text.find(GPS_LATITUDE_STRING) > 0, self.html_file.find_all("tr")))
        gps_latitude_html = gps_latitude_matches[len(gps_latitude_matches) - 1].text
        return float(re.match(GPS_LATITUDE_RE, gps_latitude_html, re.S).group(1))

    def gps_longitude(self):
        gps_longitude_matches = list(
            filter(lambda x: x.text.find(GPS_LONGITUDE_STRING) > 0, self.html_file.find_all("tr")))
        gps_longitude_html = gps_longitude_matches[len(gps_longitude_matches) - 1].text
        return float(re.match(GPS_LONGITUDE_RE, gps_longitude_html, re.S).group(1))

    def gps_coordinates(self):
        return str(self.gps_latitude()) + ', ' + str(self.gps_longitude())

    def elevation(self):
        elevation_matches = list(
            filter(lambda x: x.text.find(ELEVATION_STRING) > 0, self.html_file.find_all("tr")))

        if len(elevation_matches) < 1:
            return None

        elevation_html = elevation_matches[len(elevation_matches) - 1].text
        return float(re.match(ELEVATION_RE, elevation_html, re.S).group(1))

    def to_gpx_trackpoint(self):
        waypoint = GPXTrackPoint(self.gps_latitude(), self.gps_longitude())
        waypoint.name = self.title()
        waypoint.description = self.description()
        waypoint.comment = self.description()
        waypoint.symbol = "wpt_46"

        if self.elevation() is not None:
            waypoint.elevation = self.elevation()

        return waypoint
