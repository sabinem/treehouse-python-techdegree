import json
from collections import defaultdict, namedtuple
field_descriptor = namedtuple('Field', ['count', 'type', 'length'])

fields = defaultdict(dict)
valuesets = defaultdict(set)
occurences = defaultdict(int)


def analyze_minerals():
    with open('data/data/minerals.json') as datafile:

        mineralsjson = json.load(datafile)
        for mineral in mineralsjson:
            for key, value in mineral.items():
                occurences[key] += 1
                valuesets[key].add(value)
                if 'length' in fields[key].keys():
                    if len(value) < fields[key]['length']:
                        continue
                fields[key]['length'] = len(value)
                fields[key]['example'] = value

        with open('analyze_minerals_details.txt', 'w') as resultfile:
            for key in sorted(occurences, key = occurences.get,
                                reverse=True):
                resultfile.write("{5}\nField: {0:25s}\n{5}\noccurence: #{1:3d}, max_length: {2:3d} \nValues: {3}\nExample: {4}".format(
                    key,
                    occurences[key],
                    fields[key]['length'],
                    valuesets[key],
                    fields[key]['example'],
                    80 * '-',
                ))

        with open('analyze_minerals_summary.txt', 'w') as resultfile:
            resultfile.write("{0:25s}|{1:15s}|{2:15s}|{3:15s}\n".format(
                'Fieldname',
                'occurence count',
                'max length',
                'distinct count',
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
                    fields[key]['length'],
                    len(valuesets[key]),
                ))

if __name__ == '__main__':
    analyze_minerals()
