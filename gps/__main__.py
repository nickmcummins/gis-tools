#!/usr/bin/env python
from gps.street_address import StreetAddress

if __name__ == '__main__':
    street_address = StreetAddress('1234 Some St, City, Province')
    gpx = street_address.to_gpx()
    print(gpx)