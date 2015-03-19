#!/usr/bin/env python

import csv
import decimal
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

OUTPUT_HEADERS = [
    'state',
    'state_moe',
    'population',
    'population_white_only_nonhispanic',
    'population_white_only_nonhispanic_pct',
    'population_black_only_nonhispanic',
    'population_black_only_nonhispanic_pct',
    'population_asian_only_nonhispanic',
    'population_asian_only_nonhispanic_pct',
    'population_hispanic',
    'population_hispanic_pct',
    'population_female',
    'population_female_pct',
    'population_male',
    'population_male_pct',
    'registered',
    'registered_pct',
    'registered_white_only_nonhispanic',
    'registered_white_only_nonhispanic_pct',
    'registered_black_only_nonhispanic',
    'registered_black_only_nonhispanic_pct',
    'registered_asian_only_nonhispanic',
    'registered_asian_only_nonhispanic_pct',
    'registered_hispanic',
    'registered_hispanic_pct',
    'registered_female',
    'registered_female_pct',
    'registered_male',
    'registered_male_pct',
    'not_registered',
    'not_registered_pct',
    'not_registered_white_only_nonhispanic',
    'not_registered_white_only_nonhispanic_pct',
    'not_registered_black_only_nonhispanic',
    'not_registered_black_only_nonhispanic_pct',
    'not_registered_asian_only_nonhispanic',
    'not_registered_asian_only_nonhispanic_pct',
    'not_registered_hispanic',
    'not_registered_hispanic_pct',
    'not_registered_female',
    'not_registered_female_pct',
    'not_registered_male',
    'not_registered_male_pct',
    'unknown',
    'unknown_pct',
    'unknown_white_only_nonhispanic',
    'unknown_white_only_nonhispanic_pct',
    'unknown_black_only_nonhispanic',
    'unknown_black_only_nonhispanic_pct',
    'unknown_asian_only_nonhispanic',
    'unknown_asian_only_nonhispanic_pct',
    'unknown_hispanic',
    'unknown_hispanic_pct',
    'unknown_female',
    'unknown_female_pct',
    'unknown_male',
    'unknown_male_pct',
    'all_registered',
    'all_registered_pct',
    'all_registered_white_only_nonhispanic',
    'all_registered_white_only_nonhispanic_pct',
    'all_registered_black_only_nonhispanic',
    'all_registered_black_only_nonhispanic_pct',
    'all_registered_asian_only_nonhispanic',
    'all_registered_asian_only_nonhispanic_pct',
    'all_registered_hispanic',
    'all_registered_hispanic_pct',
    'all_registered_female',
    'all_registered_female_pct',
    'all_registered_male',
    'all_registered_male_pct',
]

def main():
    output = []

    print 'Loading data'

    table = load_data()

    print 'Computing national stats'
    output.append(compute_aggregates('United States', table))


    print 'Grouping by state'

    state_tables = table.group_by('state')

    for state, table in state_tables.items():
        print state

        output.append(compute_aggregates(state, table))

    print 'Writing output'

    write_output(output)

def load_data():
    """
    Load the initial table data from a CSV.
    """
    with open('simple.csv') as f:
        reader = csv.reader(f)
        next(reader)

        table = journalism.Table(reader, COLUMN_TYPES, COLUMN_NAMES)

    return table

def sum_weights(table):
    """
    Sum the weight column of a table to generate a population estimate.
    """
    return table.columns['weight'].sum()

def pct(numerator, denominator):
    """
    Compute a two-decimal percentage.
    """
    return (numerator / denominator * 100).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)

def compute_aggregates(state, table):
    """
    Compute aggregates for a table.
    """
    # Filter out anyone who didn't answer questions, e.g. underage (voted == -1)
    # and those who self-report they are not eligible to vote
    population_table = table.where(lambda r: r['voted'] != '-1' and r['why_not_registered'] != 'Not eligible to vote')
    population = sum_weights(population_table)
    population_white_only_nonhispanic = sum_weights(population_table.where(lambda r: r['race'] == 'White Only' and r['hispanic'] == 'Non-Hispanic'))
    population_black_only_nonhispanic = sum_weights(population_table.where(lambda r: r['race'] == 'Black Only' and r['hispanic'] == 'Non-Hispanic'))
    population_asian_only_nonhispanic = sum_weights(population_table.where(lambda r: r['race'] == 'Asian Only' and r['hispanic'] == 'Non-Hispanic'))
    population_hispanic = sum_weights(population_table.where(lambda r: r['hispanic'] == 'Hispanic'))
    population_female = sum_weights(population_table.where(lambda r: r['sex'] == 'Female'))
    population_male = sum_weights(population_table.where(lambda r: r['sex'] == 'Male'))

    registered_table = table.where(lambda r: r['voted'] == 'Yes' or r['registered'] == 'Yes')
    registered = sum_weights(registered_table)
    registered_white_only_nonhispanic = sum_weights(registered_table.where(lambda r: r['race'] == 'White Only' and r['hispanic'] == 'Non-Hispanic'))
    registered_black_only_nonhispanic = sum_weights(registered_table.where(lambda r: r['race'] == 'Black Only' and r['hispanic'] == 'Non-Hispanic'))
    registered_asian_only_nonhispanic = sum_weights(registered_table.where(lambda r: r['race'] == 'Asian Only' and r['hispanic'] == 'Non-Hispanic'))
    registered_hispanic = sum_weights(registered_table.where(lambda r: r['hispanic'] == 'Hispanic'))
    registered_female = sum_weights(registered_table.where(lambda r: r['sex'] == 'Female'))
    registered_male = sum_weights(registered_table.where(lambda r: r['sex'] == 'Male'))

    not_registered_table = table.where(lambda r: r['registered'] == 'No')
    not_registered = sum_weights(not_registered_table)
    not_registered_white_only_nonhispanic = sum_weights(not_registered_table.where(lambda r: r['race'] == 'White Only' and r['hispanic'] == 'Non-Hispanic'))
    not_registered_black_only_nonhispanic = sum_weights(not_registered_table.where(lambda r: r['race'] == 'Black Only' and r['hispanic'] == 'Non-Hispanic'))
    not_registered_asian_only_nonhispanic = sum_weights(not_registered_table.where(lambda r: r['race'] == 'Asian Only' and r['hispanic'] == 'Non-Hispanic'))
    not_registered_hispanic = sum_weights(not_registered_table.where(lambda r: r['hispanic'] == 'Hispanic'))
    not_registered_female = sum_weights(not_registered_table.where(lambda r: r['sex'] == 'Female'))
    not_registered_male = sum_weights(not_registered_table.where(lambda r: r['sex'] == 'Male'))

    unknown_table = table.where(lambda r: r['registered'] in ['Don\'t Know', 'No Response', 'Refused'])
    unknown = sum_weights(unknown_table)
    unknown_white_only_nonhispanic = sum_weights(unknown_table.where(lambda r: r['race'] == 'White Only' and r['hispanic'] == 'Non-Hispanic'))
    unknown_black_only_nonhispanic = sum_weights(unknown_table.where(lambda r: r['race'] == 'Black Only' and r['hispanic'] == 'Non-Hispanic'))
    unknown_asian_only_nonhispanic = sum_weights(unknown_table.where(lambda r: r['race'] == 'Asian Only' and r['hispanic'] == 'Non-Hispanic'))
    unknown_hispanic = sum_weights(unknown_table.where(lambda r: r['hispanic'] == 'Hispanic'))
    unknown_female = sum_weights(unknown_table.where(lambda r: r['sex'] == 'Female'))
    unknown_male = sum_weights(unknown_table.where(lambda r: r['sex'] == 'Male'))

    all_registered = registered + not_registered
    all_registered_white_only_nonhispanic = registered_white_only_nonhispanic + not_registered_white_only_nonhispanic
    all_registered_black_only_nonhispanic = registered_black_only_nonhispanic + not_registered_black_only_nonhispanic
    all_registered_asian_only_nonhispanic = registered_asian_only_nonhispanic + not_registered_asian_only_nonhispanic
    all_registered_hispanic = registered_hispanic + not_registered_hispanic
    all_registered_female = registered_female + not_registered_female
    all_registered_male = registered_male + not_registered_male

    return {
        'state': state,
        'state_moe': 'TKTK',

        'population': population,
        'population_white_only_nonhispanic': population_white_only_nonhispanic,
        'population_white_only_nonhispanic_pct': pct(population_white_only_nonhispanic, population),
        'population_black_only_nonhispanic': population_black_only_nonhispanic,
        'population_black_only_nonhispanic_pct': pct(population_black_only_nonhispanic, population),
        'population_asian_only_nonhispanic': population_asian_only_nonhispanic,
        'population_asian_only_nonhispanic_pct': pct(population_asian_only_nonhispanic, population),
        'population_hispanic': population_hispanic,
        'population_hispanic_pct': pct(population_hispanic, population),
        'population_female': population_female,
        'population_female_pct': pct(population_female, population),
        'population_male': population_male,
        'population_male_pct': pct(population_male, population),

        'registered': registered,
        'registered_pct': pct(registered, population),
        'registered_white_only_nonhispanic': registered_white_only_nonhispanic,
        'registered_white_only_nonhispanic_pct': pct(registered_white_only_nonhispanic, registered),
        'registered_black_only_nonhispanic': registered_black_only_nonhispanic,
        'registered_black_only_nonhispanic_pct': pct(registered_black_only_nonhispanic, registered),
        'registered_asian_only_nonhispanic': registered_asian_only_nonhispanic,
        'registered_asian_only_nonhispanic_pct': pct(registered_asian_only_nonhispanic, registered),
        'registered_hispanic': registered_hispanic,
        'registered_hispanic_pct': pct(registered_hispanic, registered),
        'registered_female': registered_female,
        'registered_female_pct': pct(registered_female, registered),
        'registered_male': registered_male,
        'registered_male_pct': pct(registered_male, registered),

        'not_registered': not_registered,
        'not_registered_pct': pct(not_registered, population),
        'not_registered_white_only_nonhispanic': not_registered_white_only_nonhispanic,
        'not_registered_white_only_nonhispanic_pct': pct(not_registered_white_only_nonhispanic, not_registered),
        'not_registered_black_only_nonhispanic': not_registered_black_only_nonhispanic,
        'not_registered_black_only_nonhispanic_pct': pct(not_registered_black_only_nonhispanic, not_registered),
        'not_registered_asian_only_nonhispanic': not_registered_asian_only_nonhispanic,
        'not_registered_asian_only_nonhispanic_pct': pct(not_registered_asian_only_nonhispanic, not_registered),
        'not_registered_hispanic': not_registered_hispanic,
        'not_registered_hispanic_pct': pct(not_registered_hispanic, not_registered),
        'not_registered_female': not_registered_female,
        'not_registered_female_pct': pct(not_registered_female, not_registered),
        'not_registered_male': not_registered_male,
        'not_registered_male_pct': pct(not_registered_male, not_registered),

        'unknown': unknown,
        'unknown_pct': pct(unknown, population),
        'unknown_white_only_nonhispanic': unknown_white_only_nonhispanic,
        'unknown_white_only_nonhispanic_pct': pct(unknown_white_only_nonhispanic, population),
        'unknown_black_only_nonhispanic': unknown_black_only_nonhispanic,
        'unknown_black_only_nonhispanic_pct': pct(unknown_black_only_nonhispanic, population),
        'unknown_asian_only_nonhispanic': unknown_asian_only_nonhispanic,
        'unknown_asian_only_nonhispanic_pct': pct(unknown_asian_only_nonhispanic, population),
        'unknown_hispanic': unknown_hispanic,
        'unknown_hispanic_pct': pct(unknown_hispanic, population),
        'unknown_female': unknown_female,
        'unknown_female_pct': pct(unknown_female, population),
        'unknown_male': unknown_male,
        'unknown_male_pct': pct(unknown_male, population),

        'all_registered': all_registered,
        'all_registered_pct': pct(all_registered, population),
        'all_registered_white_only_nonhispanic': all_registered_white_only_nonhispanic,
        'all_registered_white_only_nonhispanic_pct': pct(all_registered_white_only_nonhispanic, all_registered),
        'all_registered_black_only_nonhispanic': all_registered_black_only_nonhispanic,
        'all_registered_black_only_nonhispanic_pct': pct(all_registered_black_only_nonhispanic, all_registered),
        'all_registered_asian_only_nonhispanic': all_registered_asian_only_nonhispanic,
        'all_registered_asian_only_nonhispanic_pct': pct(all_registered_asian_only_nonhispanic, all_registered),
        'all_registered_hispanic': all_registered_hispanic,
        'all_registered_hispanic_pct': pct(all_registered_hispanic, all_registered),
        'all_registered_female': all_registered_female,
        'all_registered_female_pct': pct(all_registered_female, all_registered),
        'all_registered_male': all_registered_male,
        'all_registered_male_pct': pct(all_registered_male, all_registered),
    }

def write_output(output):
    """
    Write aggregate output to CSV.
    """
    with open('states.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADERS)

        writer.writeheader()
        writer.writerows(output)

if __name__ == '__main__':
    main()
