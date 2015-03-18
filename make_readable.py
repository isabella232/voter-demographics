#!/usr/bin/env python

import csv
from collections import OrderedDict

FIELD_MAPPINGS = OrderedDict([
    ('ptdtrace', {
        '1': 'White Only'
        '2': 'Black Only'
        '3': 'American Indian, Alaskan Native Only'
        '4': 'Asian Only'
        '5': 'Hawaiian/Pacific Islander Only'
        '6': 'White-Black'
        '7': 'White-AI'
        '8': 'White-Asian'
        '9': 'White-HP'
        '10': 'Black-AI'
        '11': 'Black-Asian'
        '12': 'Black-HP'
        '13': 'AI-Asian'
        '14': 'AI-HP'
        '15': 'Asian-HP'
        '16': 'W-B-AI'
        '17': 'W-B-A'
        '18': 'W-B-HP'
        '19': 'W-AI-A'
        '20': 'W-AI-HP'
        '21': 'W-A-HP'
        '22': 'B-AI-A'
        '23': 'W-B-AI-A'
        '24': 'W-AI-A-HP'
        '25': 'Other 3 Race Combinations'
        '26': 'Other 4 and 5 Race Combinations'
    }), ('pehspnon', {
        '1': 'Hispanic'
        '2': 'Non-Hispanic'
    }), ('pesex', {
        '1': 'male',
        '2': 'female'
    }), ('prtage', {
        '80': '80-84'
    }), ('pes1', {
        '1': 'Yes'
        '2': 'No'
        '-2': 'Don\'t Know'
        '-3': 'Refused'
        '-9': "No Response"
    }), ('pes2', {
        '1': 'Yes'
        '2': 'No'
        '-2': 'Don\'t Know'
        '-3': 'Refused'
        '-9': "No Response"
    }), ('pes3', {

    }), ('pes4', {

    }), ('pes5', {

    }), ('pes6', {

    }), ('pes7', {

    }), ('pes8', {

    })
])

output = []

with open('data.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        for column, mapping in FIELD_MAPPINGS.items():
            data = row[column]

            if data in mapping:
                row[column] = mapping[data]
                output.append(row)

with open('simple.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=FIELD_MAPPINGS.keys())

    writer.writeheader()
    writer.writerows(output)
