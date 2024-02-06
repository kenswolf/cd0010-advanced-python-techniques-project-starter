"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach
from helpers import cd_to_datetime


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    neos = set()

    with open(neo_csv_path) as f:
        reader = csv.reader(f)
        next(reader)  # skip header row

        for row in reader:

            # primary designation of the NEO. A unique identifier in db, and "name" to computer systems.
            designation = row[3]

            # whether NASA has marked the NEO as a "Potentially Hazardous Asteroid"
            pha = (row[7] == 'Y')

            # International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
            if row[4] == '':
                name = None
            else:
                name = row[4]

            # the NEO's diameter (from an equivalent sphere) in kilometers.
            if row[15] == '':
                diameter = float('nan')
            else:
                diameter = float(row[15])

            neos.add(NearEarthObject(designation, name, diameter, pha))

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """

    approaches = set()

    with open(cad_json_path) as f:
        json_data = json.load(f)
        data = json_data["data"]
        for cad in data:
            # ["des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf", "t_sigma_f", "h"]
            designation = cad[0]  # des - primary designation of the NEO.
            # cd - time of close-approach (formatted calendar date/time, in UTC)
            time = cd_to_datetime(cad[3])
            distance = float(cad[4])  # dist - nominal approach distance (au)
            # v_rel - velocity relative to the approach body at close approach (km/s)
            velocity = float(cad[7])
            ca = CloseApproach(designation, time, distance, velocity)
            approaches.add(ca)

    return approaches
