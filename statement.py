#!/usr/bin/env python3
# coding=utf-8

import datetime
import locale

from config import read_config
from transactions import from_csv as transactions_from_csv

locale.setlocale(locale.LC_ALL, 'en_GB')


def read_statement(transactions_file):
    config = read_config()

    # Transactions
    transactions = transactions_from_csv(transactions_file)
    # for transaction in transactions:
    #     transaction.compute_categories(config['matchers'])

    # Analysis
    monthly = {}
    for transaction in transactions:
        month = datetime.date.strftime(transaction.date, '%Y-%m')
        if month not in monthly:
            monthly[month] = []
        monthly[month].append(transaction)

    for month, transactions in sorted(monthly.items(), key=lambda x: x[0]):
        categorized = {}
        un_categorized = []
        for transaction in transactions:
            if len(transaction.categories) == 1:
                category = transaction.categories[0]
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(transaction)
            else:
                un_categorized.append(transaction)

        montly_total_debit = sum(transaction.value for transaction in transactions if transaction.value > 0)
        montly_total_credit = sum(transaction.value for transaction in transactions if transaction.value < 0)
        print()
        print('{}: Dr {:.2f} Cr {:.2f}'.format(month, montly_total_debit, montly_total_credit))
        categorized['un-categorized'] = un_categorized
        for category, categorized_transactions in categorized.items():
            debit = sum(transaction.value for transaction in categorized_transactions if transaction.value > 0)
            credit = sum(transaction.value for transaction in categorized_transactions if transaction.value < 0)
            print('\t{}\tDr {:.2f} Cr {:.2f}'.format(category, debit, credit))


def run():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=open, help='Input file')
    args = parser.parse_args()

    if args.file:
        read_statement(args.file)


if __name__ == '__main__':
    run()
