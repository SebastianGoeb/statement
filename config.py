import csv
import os

CONFIG_PATH = os.path.expanduser('~/.config/statement/config.tsv')


def _matcher(headers, row):
    row_dict = dict(zip(headers, row))
    regexes = dict(filter(lambda x: x[0] not in ['name', 'category'] and x[1], row_dict.items()))
    return {
        'name': row_dict['name'],
        'category': row_dict['category'],
        'regexes': regexes
    }


def read_config():
    if not os.path.exists(CONFIG_PATH):
        return []

    reader = csv.reader(open(CONFIG_PATH), delimiter='\t')
    headers = None
    matchers = []
    non_empty_rows = filter(lambda x: x, reader)
    for row in non_empty_rows:
        if not headers:
            headers = row
        else:
            matchers.append(_matcher(headers, row))
    return {
        'matchers': matchers
    }


def save_config(config):
    if not os.path.exists(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))

    writer = csv.writer(open(CONFIG_PATH, 'w'), delimiter='\t')

    matchers = config['matchers']
    regex_names = list(sorted(set(header for matcher in matchers for header in matcher['regexes'])))
    headers = ['name', 'category'] + regex_names

    writer.writerow(headers)

    for matcher in config['matchers']:
        row = [matcher['name'], matcher['category']] + [matcher['regexes'].get(name) for name in regex_names]
        writer.writerow(row)
