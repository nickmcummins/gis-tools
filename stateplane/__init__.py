import argparse

from math import floor
from gpxpy.gpx import GPX, GPXTrackPoint
from pyproj import Proj, transform

epsg_42148 = '+proj=lcc +lat_1=47.5 +lat_2=48.73333333333333 +lat_0=47 +lon_0=-120.8333333333333 ' \
             '+x_0=500000.0000000002 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs'


def stateplane_to_latlon(x1, y1):
    in_proj = Proj(epsg_42148, preserve_units=True)
    out_proj = Proj(init='epsg:4326')

    x2, y2 = transform(in_proj, out_proj, x1, y1)
    return x2, y2


def csv_line_to_gpx(csv_line):
    attrs = csv_line.split(',')
    lat, lng = stateplane_to_latlon(float(attrs[1]), float(attrs[2]))
    trackpoint = GPXTrackPoint(lat, lng)
    trackpoint.name = 'Tree ' + str(floor(float(attrs[4]))) + '"'
    return trackpoint


def main(csv_file):
    with open(csv_file) as f:
        lines = f.readlines()

    csv_lines = lines[1:]

    gpx = GPX()

    for tree_csv in csv_lines:
        gpx.waypoints.append(csv_line_to_gpx(tree_csv))

    output_file = open('canopymaxima_trees.gpx', 'w')
    output_file.write(gpx.to_xml())
    output_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Convert a FUSION tree .csv file to .gpx format')
    parser.add_argument('csv', type=str, nargs='+')
    args = parser.parse_args()
    main(args.csv[0])
