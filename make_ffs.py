#!/usr/bin/env python

import csv

HEADERS = ['column', 'start', 'length', 'description']
rows = []

with open('data_layout_simplified.sps') as f:
    for line in f:
        line = line.replace(' (a)', '')

        bits = line.split(' ')

        name = bits[0]
        columns = bits[-1]

        print name, columns

        if '-' in columns:
            parts = columns.split('-')

            first = int(parts[0])
            last = int(parts[1])
        else:
            first = int(columns)
            last = first

        rows.append([
            name,
            # Convert to zero base
            first - 1,
            # Ranges are inclusive, but need to be zero base
            last - first + 1,
            name
        ])

with open('schema.csv', 'w') as f:
    writer = csv.writer(f)

    writer.writerow(HEADERS)
    writer.writerows(rows)
