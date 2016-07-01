#!/usr/bin/env python3

import argparse
from gps.street_address import StreetAddress

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('address', nargs='+')
    args = parser.parse_args()
    address_string = ' '.join(args.address)

    street_address = StreetAddress(address_string)
    gpx = street_address.to_gpx()
    print(gpx)