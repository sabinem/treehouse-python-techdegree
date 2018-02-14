"""
Helper programm to analyze the data in
minerals.json.
"""
import json
import os
from collections import defaultdict

from mineral_catalog.settings import DATA_DIR


def analyze_minerals():
    """
    Analyzes the minerals.json file and outputs two text files.
    A summary contains the aggregations and answers which field
    occured how often, with how many distinct values and what was
    the maximum length.
    A detail file contains all  distinct values for each field that
    occured in the data.
    """
    datapath = os.path.join(DATA_DIR, 'minerals.json')
    with open(datapath) as datafile:

        fields = defaultdict(dict)
        valuesets = defaultdict(set)
        occurences = defaultdict(int)

        mineralsjson = json.load(datafile)

        for mineral in mineralsjson:
            for key, value in mineral.items():
                if value != '':
                    occurences[key] += 1
                    valuesets[key].add(value)
                    if 'length' in fields[key].keys():
                        if len(value) < fields[key]['length']:
                            continue
                    fields[key]['length'] = len(value)
                    fields[key]['example'] = value

        with open('data_details.txt', 'w') as resultfile:
            for key in sorted(occurences,
                              key=occurences.get,
                              reverse=True):
                resultfile.write(
                    "{4}\nField: {0:25s}\n{4}\noccurence: #{1:3d}, max_length: {2:3d} \nValues: {3}\n"
                    .format(
                        key,
                        occurences[key],
                        fields[key]['length'],
                        valuesets[key],
                        80 * '-',
                    )
                )

        with open('data_summary.txt', 'w') as resultfile:
            resultfile.write("{0:25s}|{1:15s}|{2:15s}|{3:15s}\n".format(
                'Fieldname',
                'occurence count',
                'distinct count',
                'max length',
            ))
            resultfile.write("{0:25s}|{1:15s}|{1:15s}|{1:15s}\n".format(
                25 * '-',
                15 * '-',
            ))
            for key in sorted(occurences, key=occurences.get,
                              reverse=True):

                resultfile.write("{0:25s}|{1:15d}|{2:15d}|{3:15d}\n".format(
                    key,
                    occurences[key],
                    len(valuesets[key]),
                    fields[key]['length'],
                ))

if __name__ == '__main__':
    analyze_minerals()
