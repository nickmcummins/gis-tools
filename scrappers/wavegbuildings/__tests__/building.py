import unittest
from unittest.mock import MagicMock

from gps.gps_address_converter import GPSAddressConverter
from scrappers.wavegbuildings.building import Building


class BuildingTest(unittest.TestCase):

    def test_to_gpx_trackpoint(self):
        geocoder = GPSAddressConverter()
        geocoder.convert = MagicMock(return_value={'lat': 'some latitude', 'lng': 'some longitude'})
        building = Building("a building name", "1000 2nd Ave, Seattle, WA 98104", "Gigabit and 100 MBps", geocoder)
        gpx = building.to_gpx_trackpoint()
        self.assertEquals(gpx.name, "a building name")
        self.assertEquals(gpx.latitude, "some latitude")
        self.assertEquals(gpx.longitude, "some longitude")


if __name__ == "__main__":
    unittest.main()
