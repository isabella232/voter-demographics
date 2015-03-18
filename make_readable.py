#!/usr/bin/env python

import csv
from collections import OrderedDict

FIELD_MAPPINGS = OrderedDict([
    ('ptdtrace', {
        ''
    }), ('pehspnon', {

    }), ('pesex', {
        '1': 'male',
        '2': 'female'
    }), ('prtage', {

    }), ('pes1', {

    }), ('pes2', {

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
