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


def load_neos(neo_csv_path='data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    neo_lst = []
    with open(neo_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            designation = row['pdes']

            if row['name'] == '':
                name = None
            else:
                name = row['name']

            if row['diameter'] == '':
                diameter = float('nan')
            else:
                diameter = float(row['diameter'])

            if row['pha'] == 'Y':
                hazardous = True
            else:
                hazardous = False
            neo = NearEarthObject(designation, name, diameter, hazardous)
            neo_lst.append(neo)
    return neo_lst


def load_approaches(cad_json_path='data/cad.json'):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """

    ca_lst = []
    with open(cad_json_path, 'r') as f:
        reader = json.load(f)
        for row in reader['data']:
            time = row[3]
            distance = float(row[4])
            velocity = float(row[7])
            designation = row[0]

            ca = CloseApproach(time, distance, velocity, designation)
            ca_lst.append(ca)
    return ca_lst
