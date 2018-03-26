import csv
import functools
import itertools
import logging

import os
import re

import sys
from collections import OrderedDict, namedtuple

logger = logging.getLogger(__name__)

LENGTHS = [249163442, 243078003, 197813415, 191015739, 180695227, 170959304, 159091448, 146137372, 141069069,
           135430928, 134747460, 133630123, 96085774, 87668527, 82491127, 90079543, 81032226, 78003657, 58843222,
           62887650, 37234222, 35178458]


def sum_chrs(lengths, columns):
    logging.debug('lengths: %s', lengths)
    logging.debug('columns: %s', columns)
    column_values = [float(column[1]) for column in columns]
    result = sum(column_values)
    logging.debug('result: %s', result)
    return result


def get_chromosome_length_for_column_name(lengths, column_name):
    """Get the chromosome length for a column name
    >>> lengths = [249163442, 243078003, 197813415, 191015739, 180695227, 170959304, 159091448, 146137372, 141069069, \
    135430928, 134747460, 133630123, 96085774, 87668527, 82491127, 90079543, 81032226, 78003657, 58843222, 62887650, \
    37234222, 35178458]
    >>> get_chromosome_length_for_column_name(lengths, 'TajD_C_CGI_chr1')
    249163442
    >>> get_chromosome_length_for_column_name(lengths, 'TajD_C_CGI_chr2')
    243078003
    >>> get_chromosome_length_for_column_name(lengths, 'TajD_C_CGI_chr23')
    Traceback (most recent call last):
      ...
      File "<module>", in get_chromosome_length_for_column_name
        assert 1 <= chromosome_number <= 22, 'Invalid chromosome number: %d' % chromosome_number
    AssertionError: Invalid chromosome number: 23
    >>> get_chromosome_length_for_column_name(lengths, 'TajD_D_CGI_sum')
    Traceback (most recent call last):
      ...
    ValueError: ('Column name does not end in `_chr[1-22]`: %s', 'TajD_D_CGI_sum')

    :param lengths: The chromosome lengths
    :type lengths: list(int)
    :param column_name: Name of a column, something like 'TajD_C_CGI_chr1'
    :type column_name: str
    :return: A chromosome length
    :rtype: int
    """
    assert isinstance(column_name, str)
    pattern = re.compile(r'^.+_chr(\d+)$')
    match = pattern.match(column_name)
    if not match:
        raise ValueError('Column name does not end in `_chr[1-22]`: %s', column_name)
    chromosome_string = match.groups()[0]
    logging.debug('chromosome_string: %s', chromosome_string)
    chromosome_number = int(chromosome_string)
    assert 1 <= chromosome_number <= 22, 'Invalid chromosome number: %d' % chromosome_number
    chromosome_length = lengths[chromosome_number - 1]
    assert isinstance(chromosome_length, int)
    return chromosome_length


def relative_value_chr(lengths, genome_length, column):
    logging.debug('lengths: %s', lengths)
    logging.debug('column: %s', column)
    logging.debug('genome_length: %s', genome_length)
    column_name, column_value_str = column
    column_value = float(column_value_str)
    chromosome_length = get_chromosome_length_for_column_name(lengths, column_name)
    logging.debug('chromosome_length: %s', chromosome_length)
    relative_value = column_value * float(chromosome_length) / genome_length
    return relative_value


def relative_sum_chrs(lengths, columns):
    logging.debug('lengths: %s', lengths)
    logging.debug('columns: %s', columns)
    genome_length = sum(lengths)
    logging.debug('genome_length: %s', genome_length)
    relative_value_chr_partial = functools.partial(relative_value_chr, lengths, genome_length)
    relative_values = map(relative_value_chr_partial, columns)
    logging.debug('relative_values: %s', [rv for rv in relative_values])
    result = sum(relative_values)
    return result


# Any column with ‘TajD’, ‘FST’, ‘Pi’ is `relative_sum_chrs` and any column with ‘Seg’, ‘Sing’, ‘Dupl’ is `sum_chrs`

CALCULATION_META_CONFIG = [
    {
        'input_columns_prefixes': ['TajD', 'FST', 'Pi'],
        'function': relative_sum_chrs,
        'output_column_postfix': '_relative_sum_chrs'
    },
    {
        'input_columns_prefixes': ['Seg', 'Sing', 'Dupl'],
        'function': sum_chrs,
        'output_column_postfix': '_sum'
    }
]


def main(genome_results_file):
    logging.debug('genome_results_file = %s', genome_results_file)
    calculation_config = generate_calculation_config(CALCULATION_META_CONFIG)
    partial_calculation_function = functools.partial(apply_all_calculations_to_row, calculation_config, LENGTHS)

    with open(genome_results_file) as csvfile:
        logging.debug('csvfile = %s', csvfile)
        reader = csv.DictReader(csvfile, delimiter='\t')
        logging.debug('reader = %s', reader)
        assert isinstance(reader, csv.DictReader)
        output_rows = map(partial_calculation_function, reader)

        first_output_row = next(output_rows)
        assert isinstance(first_output_row, OrderedDict)
        output_field_names = first_output_row.keys()
        logging.debug('output_field_names = %s', output_field_names)
        writer = csv.DictWriter(sys.stdout, output_field_names, dialect=csv.excel_tab)
        writer.writeheader()
        writer.writerow(first_output_row)
        writer.writerows(output_rows)


CalculationConfigItem = namedtuple('CalculationConfigItem',
                                   ['input_column_prefix', 'function', 'output_column_postfix'])


def generate_calculation_config(calculation_meta_config):
    """Generate calculation config items from the meta configuration

    >>> CALCULATION_META_CONFIG = [
    ...     {
    ...         'input_columns_prefixes': ['TajD', 'FST', 'Pi'],
    ...         'function': relative_sum_chrs,
    ...         'output_column_postfix': '_relative_sum_chrs'
    ...     },
    ...     {
    ...         'input_columns_prefixes': ['Seg', 'Sing', 'Dupl'],
    ...         'function': sum_chrs,
    ...         'output_column_postfix': '_sum'
    ...     }
    ... ]
    >>> calculation_config = generate_calculation_config(CALCULATION_META_CONFIG)
    >>> for config_item in calculation_config:
    ...     print(config_item)  #doctest: +ELLIPSIS
    CalculationConfigItem(input_column_prefix='TajD', function=<function relative_sum_chrs at 0x...>, output_column_postfix='_relative_sum_chrs')
    CalculationConfigItem(input_column_prefix='FST', function=<function relative_sum_chrs at 0x...>, output_column_postfix='_relative_sum_chrs')
    CalculationConfigItem(input_column_prefix='Pi', function=<function relative_sum_chrs at 0x...>, output_column_postfix='_relative_sum_chrs')
    CalculationConfigItem(input_column_prefix='Seg', function=<function sum_chrs at 0x...>, output_column_postfix='_sum')
    CalculationConfigItem(input_column_prefix='Sing', function=<function sum_chrs at 0x...>, output_column_postfix='_sum')
    CalculationConfigItem(input_column_prefix='Dupl', function=<function sum_chrs at 0x...>, output_column_postfix='_sum')

    :param calculation_meta_config: A list of dicts
    :type calculation_meta_config: list<dict>
    :return: A list of CalculationConfigItems
    :rtype: list<CalculationConfigItem>
    """
    calculation_config = []
    for meta_config_item in calculation_meta_config:
        config_function = meta_config_item['function']
        output_column_postfix = meta_config_item['output_column_postfix']
        for input_column_prefix in meta_config_item['input_columns_prefixes']:
            calculation_config_item = CalculationConfigItem(input_column_prefix, config_function, output_column_postfix)
            calculation_config.append(calculation_config_item)
    return calculation_config


def apply_single_calculation_to_column_group(lengths, calculation_config, column_group):
    logging.debug('column_group: %s', column_group)
    logging.debug('calculation_config: %s', calculation_config)
    logging.debug('lengths: %s', lengths)
    assert isinstance(column_group, tuple)
    assert len(column_group) == 2

    group_prefix = column_group[0]
    assert isinstance(group_prefix, str)
    columns = column_group[1]
    assert isinstance(columns, list)
    calculation_config_items = [c for c in calculation_config if group_prefix.startswith(c.input_column_prefix)]
    assert len(calculation_config_items) == 1
    calculation_config_item = calculation_config_items[0]
    assert isinstance(calculation_config_item, CalculationConfigItem)
    calculation_function = calculation_config_item.function
    calculation_result = calculation_function(lengths, columns)
    calculation_name = '{}{}'.format(group_prefix, calculation_config_item.output_column_postfix)
    return calculation_name, calculation_result


def summary_stat_prefix(column_tuple):
    """Key function to group related summary stats across chromosomes
    >>> summary_stat_prefix(('Dupl_A_CGI_chr1', 1234))
    'Dupl_A_CGI'
    >>> summary_stat_prefix(('Dupl_A_CGI_chr22', 312))
    'Dupl_A_CGI'
    >>> summary_stat_prefix(('Dupl_A_CGI_sum', 4321))
    'Dupl_A_CGI'
    >>> summary_stat_prefix(('Dupl_A_CGI_relative_sum', 1234))
    'Dupl_A_CGI'
    >>> summary_stat_prefix(('Dupl_B_CGI_chr1', 431))
    'Dupl_B_CGI'
    >>> summary_stat_prefix(('Some_Unexpected_String', 4312))
    'Some_Unexpected_String'
    >>> summary_stat_prefix(('A', 431))
    'A'

    :param column_tuple: Something like ('Dupl_A_CGI_chr1', 1234) or ('A', 431)
    :type column_tuple: tuple
    :return: Something like 'Dupl_A_CGI' or 'A'
    :rtype: str
    """
    logging.debug('column_tuple: %s', column_tuple)
    assert isinstance(column_tuple, tuple)
    assert len(column_tuple) == 2
    column_name = column_tuple[0]
    groupby_key = column_name
    patterns = (
        re.compile(r'(^.+)_chr\d+$'),
        re.compile(r'(^.+)_relative_sum$'),
        re.compile(r'(^.+)_sum$')
    )
    for pattern in patterns:
        match = pattern.match(column_name)
        if match:
            groupby_key = match.groups()[0]
            break
    return groupby_key


def summary_stat_matches_column_prefixes(column_prefixes, column_name):
    """If `column_name` ends with `_chr[1-22]` and starts with any of the the configured column prefixes, return True,
    otherwise return False.

    >>> column_prefixes = ['TajD', 'FST', 'Pi', 'Seg', 'Sing', 'Dupl']
    >>> summary_stat_matches_column_prefixes(column_prefixes, 'Dupl_A_CGI_chr1')
    True
    >>> summary_stat_matches_column_prefixes(column_prefixes, 'Dupl_A_CGI_chr22')
    True
    >>> summary_stat_matches_column_prefixes(column_prefixes, 'Sing_B_CGI_chr2')
    True
    >>> summary_stat_matches_column_prefixes(column_prefixes, 'Dupl_A_CGI_sum')
    False
    >>> summary_stat_matches_column_prefixes(column_prefixes, 'Dupl_A_CGI_relative_sum')
    False
    >>> summary_stat_matches_column_prefixes(column_prefixes, 'A')
    False

    :param column_prefixes: A collection of configured column prefixes
    :type column_prefixes: list(str)
    :param column_name: Something like 'Dupl_A_CGI_chr1' or 'A'
    :type column_name: str
    :return: Whether column_name matches any of the column prefixes, and ends with `_chr[1-22]`
    :rtype: bool
    """
    assert isinstance(column_name, str)
    pattern = re.compile(r'(^.+)_chr\d+$')
    match = pattern.match(column_name)
    if not match:
        # column_name doesn't end with `_chr[1-22]` so return False
        return False

    matching_configured_columns = [column_name.startswith(prefix) for prefix in column_prefixes]
    return any(matching_configured_columns)


def group_columns_by_summary_stats(columns):
    """Group all chromosome columns by the summary statistic name

    >>> columns = [
    ... ('SegS_A_CGI_chr1', 11),
    ... ('SegS_A_CGI_chr2', 12),
    ... ('SegS_A_CGI_chr3', 13),
    ... ('Sing_A_CGI_chr1', 21),
    ... ('Sing_A_CGI_chr2', 22),
    ... ('Sing_A_CGI_chr3', 23),
    ... ('Dupl_A_CGI_chr1', 31),
    ... ('Dupl_A_CGI_chr2', 32),
    ... ('Dupl_A_CGI_chr3', 33)
    ... ]
    >>> column_groups = group_columns_by_summary_stats(columns)
    >>> for cg in column_groups:
    ...     print(cg)
    ('SegS_A_CGI', [('SegS_A_CGI_chr1', 11), ('SegS_A_CGI_chr2', 12), ('SegS_A_CGI_chr3', 13)])
    ('Sing_A_CGI', [('Sing_A_CGI_chr1', 21), ('Sing_A_CGI_chr2', 22), ('Sing_A_CGI_chr3', 23)])
    ('Dupl_A_CGI', [('Dupl_A_CGI_chr1', 31), ('Dupl_A_CGI_chr2', 32), ('Dupl_A_CGI_chr3', 33)])

    Note that you they have to be sorted first:
    https://docs.python.org/3/library/itertools.html#itertools.groupby
    ...otherwise you get this situation below:

    >>> columns = [
    ... ('SegS_A_CGI_chr1', 11),
    ... ('Sing_A_CGI_chr1', 21),
    ... ('Dupl_A_CGI_chr1', 31),
    ... ('SegS_A_CGI_chr2', 12),
    ... ('Sing_A_CGI_chr2', 22),
    ... ('Dupl_A_CGI_chr2', 32),
    ... ('SegS_A_CGI_chr3', 13),
    ... ('Sing_A_CGI_chr3', 23),
    ... ('Dupl_A_CGI_chr3', 33)
    ... ]
    >>> column_groups = group_columns_by_summary_stats(columns)
    >>> for cg in column_groups:
    ...     print(cg)
    ('SegS_A_CGI', [('SegS_A_CGI_chr1', 11)])
    ('Sing_A_CGI', [('Sing_A_CGI_chr1', 21)])
    ('Dupl_A_CGI', [('Dupl_A_CGI_chr1', 31)])
    ('SegS_A_CGI', [('SegS_A_CGI_chr2', 12)])
    ('Sing_A_CGI', [('Sing_A_CGI_chr2', 22)])
    ('Dupl_A_CGI', [('Dupl_A_CGI_chr2', 32)])
    ('SegS_A_CGI', [('SegS_A_CGI_chr3', 13)])
    ('Sing_A_CGI', [('Sing_A_CGI_chr3', 23)])
    ('Dupl_A_CGI', [('Dupl_A_CGI_chr3', 33)])
    """
    logging.debug('columns: %s', columns)
    input_columns_grouped = ((key, list(group)) for key, group in itertools.groupby(columns, summary_stat_prefix))
    return input_columns_grouped


def apply_all_calculations_to_row(calculation_config, lengths, input_row):
    """Calculate the summary statistics over the chromosomes

    :param calculation_config: List of CalculationConfigItem objects
    :type calculation_config: list(CalculationConfigItem)
    :param lengths: Lengths of the chromosomes
    :type lengths: list(int)
    :param input_row: A row from the summary stats file
    :type input_row: collections.OrderedDict
    :return: The input row with the calculated columns added
    :rtype: collections.OrderedDict
    """
    logging.debug('calculation_config: %s', calculation_config)
    logging.debug('lengths: %s', lengths)
    logging.debug('input_row: %s', input_row)
    configured_column_prefixes = [config_item.input_column_prefix for config_item in calculation_config]
    logging.debug('configured_column_prefixes: %s', configured_column_prefixes)
    filter_function = functools.partial(summary_stat_matches_column_prefixes, configured_column_prefixes)
    input_column_names = sorted(filter(filter_function, input_row))
    input_columns = [(column_name, input_row[column_name]) for column_name in input_column_names]
    logging.debug('input_columns: %s', [ic for ic in input_columns])

    input_column_groups = group_columns_by_summary_stats(input_columns)
    logging.debug('input_column_groups: %s', input_column_groups)

    partial_single_calculation_function = functools.partial(apply_single_calculation_to_column_group, lengths,
                                                            calculation_config)
    calculations = map(partial_single_calculation_function, input_column_groups)
    output_row = input_row
    assert isinstance(output_row, OrderedDict)
    output_row.update(calculations)
    logging.debug('output_row: %s', output_row)
    return output_row


if __name__ == '__main__':
    LOGGING_FORMAT = "%(levelname)s:%(name)s:%(funcName)s:%(lineno)d:%(message)s"
    logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'), format=LOGGING_FORMAT)
    logging.debug('START')
    # TODO: Pass in the file name as a command-line argument, and/or read from `stdin`
    main('head_final_results.tsv')
    logging.debug('END')
