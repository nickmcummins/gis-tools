import sys
from lxml import etree
import argparse

import gpxpy
import geopy.distance

SECONDS_PER_HOUR = 3600

def latlon(gpx_point):
    return (gpx_point.latitude, gpx_point.longitude)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter GPX track points')
    parser.add_argument('gpxfilename', help='the GPX file to filter')
    parser.add_argument('-s', '--speed', default=100, help='the speed threshold for discarding points')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('-o', '--output', default=None, help='the name of the output file for the filtered GPX')

    args = parser.parse_args()
    gpx_filename = args.gpxfilename
    gpx_file = open(gpx_filename)
    gpx = gpxpy.parse(gpx_file)

    segment = gpx.tracks[0].segments[0]
    completed = False

    while not completed:
        removed_points = 0
        for i in range(1, len(segment.points)):
            point = segment.points[i - removed_points]
            prev_point = segment.points[i - 1 - removed_points]
            distance = geopy.distance.geodesic(latlon(point), latlon(prev_point))
            if distance.feet < 500:
                display_distance = f'{int(distance.feet)} ft'
            else:
                display_distance = f'{distance.miles:.1f} mi'
            duration = point.time - prev_point.time
            mph = int(distance.mi / (duration.seconds / SECONDS_PER_HOUR)) if duration.seconds > 0 else 0
            if mph > args.speed:
                segment.remove_point(i - 1 - removed_points)
                removed_points += 1
                if args.verbose:
                    print(f'removing point: {point.time}\t({point.latitude},{point.longitude})\t{display_distance}\t{duration}\t{mph} mph')
        print(f'removed {removed_points} points over 100 mph.')
        if removed_points == 1:
            completed = True

    filtered_gpx_filename = gpx_filename.replace('.gpx', '_filtered.gpx') if args.output is None else args.output
    with open(filtered_gpx_filename, 'w') as filtered_gpxfile:
        filtered_gpxfile.write(etree.tostring(etree.fromstring(gpx.to_xml().encode('utf-8'), parser=etree.XMLParser(encoding='utf-8')), pretty_print=True).decode('utf-8'))