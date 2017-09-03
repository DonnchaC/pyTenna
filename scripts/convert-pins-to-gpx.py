#!/usr/bin/env python
"""
Convert the goTenna generated Pins.json file to a standard GPX track.

The Pins.jsom file must be decrypted using the decryption script before
it can be used to plot the GPX track.
"""

import argparse
import json
import datetime

import gpxpy
import gpxpy.gpx


def gpx_from_pin_data(pin_data):
    gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Create points:
    for point in pin_data:
        timestamp = datetime.datetime.fromtimestamp(point["gpsTimestamp"] / 1000)
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point["latitude"], point["longitude"],
                                                          name=point["name"], time=timestamp))

    # You can add routes and waypoints, too
    return gpx.to_xml()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create GPX from Pins.json.')
    parser.add_argument('file', metavar='FILE', type=str, help='Pin file', default='Pins.json')
    args = parser.parse_args()

    with open(args.file, "r") as pin_file:
        pin_data = json.loads(pin_file.read())

    print(gpx_from_pin_data(pin_data))
