#!/usr/bin/env python

import csv
from collections import OrderedDict

STATES = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}

FIPS = { v: k for k, v in STATES.items() }

FIELD_MAPPINGS = OrderedDict([
    ('gestfips', FIPS),
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
        '1': 'Male',
        '2': 'Female'
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
        '1': 'Missed deadline',
        '2': 'Did not know how or where to register',
        '3': 'Did not meet residency requirements',
        '4': 'Permanent illness',
        '5': 'Difficulty with English',
        '6': 'Not interested in election',
        '7': 'Vote would not make a difference',
        '8': 'Not eligible to vote',
        '9': 'Other reason',
        '-2': 'Don\'t know',
        '-3': 'Refused',
        '-9': 'No response'
    }), ('pes4', {
        '1': 'Illness',
        '2': 'Out of town',
        '3': 'Forgot',
        '4': 'Not interested',
        '5': 'Too busy',
        '6': 'Transporationt problem',
        '7': 'Didn\'t like candidates',
        '8': 'Registration problems',
        '9': 'Bad weather',
        '10': 'Inconvenient hours or locations',
        '11': 'Other',
        '-2': 'Don\'t know',
        '-3': 'Refused',
        '-9': 'No response'
    }), ('pes5', {
        '1': 'In person',
        '2': 'By mail',
        '-2': 'Don\'t know',
        '-3': 'Refused',
        '-9': 'No response'
    }), ('pes6', {
        '1': 'On election day',
        '2': 'Before election day',
        '-2': 'Don\'t know',
        '-3': 'Refused',
        '-9': 'No response'
    }), ('pes7', {
        '1': 'DMV',
        '2': 'Medicaid or other agency',
        '3': 'Mail',
        '4': 'Internet',
        '5': 'School or Hospital',
        '6': 'Town hall or county office',
        '7': 'Registration drive',
        '8': 'Polling place',
        '9': 'Other',
        '-2': 'Don\'t know',
        '-3': 'Refused',
        '-9': 'No response'
    }), ('pes8', {
        '1': 'Less than 1 month',
        '2': '1-6 months',
        '3': '7-11 months',
        '4': '1-2 years',
        '5': '3-4 years',
        '6': '5+ years',
        '-2': 'Don\'t know',
        '-3': 'Refused',
        '-9': 'No response'
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
