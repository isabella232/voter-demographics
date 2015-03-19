#!/usr/bin/env python

import csv
import journalism

text_type = journalism.TextType()
number_type = journalism.NumberType()

COLUMNS = (
    ('weight', number_type),
    ('state', text_type),
    ('race', text_type),
    ('hispanic', text_type),
    ('sex', text_type),
    ('age', text_type),
    ('voted', text_type),
    ('registered', text_type),
    ('why_not_registered', text_type),
    ('why_not_vote', text_type),
    ('voted_how', text_type),
    ('voted_on_election_day', text_type),
    ('registered_how', text_type),
    ('lived_at_current_address', text_type),
)

COLUMN_NAMES = [c[0] for c in COLUMNS]
COLUMN_TYPES = [c[1] for c in COLUMNS]

with open('simple.csv') as f:
    reader = csv.reader(f)
    next(reader)

    table = journalism.Table(reader, COLUMN_TYPES, COLUMN_NAMES)

table = table.where(lambda r: r['state'] == 'TX')

print 'DC!', table.columns['weight'].sum()

#voted = table.where(lambda r: r['voted'] == 'Yes')

#print 'Voted:', sum([r['weight'] for r in voted.rows])

#eligible_to_register = table.where(lambda r: r['registered'] == 'No' and r['why_not_registered'] != 'Not eligible to vote')

#print 'Eligible to register:', len(eligible_to_register.rows)

registered = table.where(lambda r: r['voted'] == 'Yes' or r['registered'] == 'Yes')

print 'Registered:', registered.columns['weight'].sum()

not_registered = table.where(lambda r: r['registered'] == 'No')

print 'Not registered:', not_registered.columns['weight'].sum()

#states = answered_voting_questions.group_by('state')

#for state, table in states.items():

african_american = table.where(lambda r: r['race'] == 'Black Only' and r['hispanic'] == 'Non-Hispanic')

print 'Black:',  african_american.columns['weight'].sum()

white = table.where(lambda r: r['race'] == 'White Only' and r['hispanic'] == 'Non-Hispanic')

print 'White:', white.columns['weight'].sum()
