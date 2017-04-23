import csv
import re
from datetime import datetime

DATE_COLUMN = 'Date'
TYPE_COLUMN = ' Type'
DESCRIPTION_COLUMN = ' Description'
VALUE_COLUMN = ' Value'
BALANCE_COLUMN = ' Balance'
ACCOUNT_NAME_COLUMN = ' Account Name'
ACCOUNT_NUMBER_COLUMN = ' Account Number'

DATE_FORMAT = '%d/%m/%Y'


class Transaction(object):
    def __init__(self, csv_row):
        self.date = datetime.strptime(csv_row[DATE_COLUMN], DATE_FORMAT).date()
        self.type = csv_row[TYPE_COLUMN]
        self.description = csv_row[DESCRIPTION_COLUMN]
        self.value = float(csv_row[VALUE_COLUMN])
        self.balance = float(csv_row[BALANCE_COLUMN])
        self.account_name = csv_row[ACCOUNT_NAME_COLUMN]
        self.account_number = csv_row[ACCOUNT_NUMBER_COLUMN]
        self.categories = []

        # self.matchers = extract_matchers(csv_row, matchers)
        # self.categories = extract_categories(transaction['matchers'], categories)

    def __str__(self):
        return '{:<16} {:<8} {}'.format(str(self.date), self.value, self.description)

    # def matches(self, matcher):
    #     regexes = matcher['regexes']
    #
    #     return all(True for regex in regexes.values())
    #
    # def compute_categories(self, matchers):
    #     self.categories = [matcher['category'] for matcher in matchers if self.matches(matcher)]


def from_csv(transactions_file):
    reader = csv.reader(transactions_file, dialect='excel')
    headers = None
    non_empty_rows = filter(lambda x: x, reader)
    for row in non_empty_rows:
        if not headers:
            headers = row
        else:
            transaction = Transaction(dict(zip(headers, row)))
            yield transaction

def categorize():
    pass
