# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 11, 2018

from __future__ import print_function # to run this code under python27
from collections import defaultdict
import csv
import math
import sys

import parser # my module


def donorID(name, zip_code):
    """User is identified by its name and zip_code only"""
    return (name, zip_code)


def recipientID(recipient, zip_code, year):
    """recipient from zip_code at year"""
    return (recipient, zip_code, year)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python", __file__,
              "input_file percentile_file output_file")
        exit(0)

    fname_itcont = sys.argv[1]
    fname_percentile = sys.argv[2]
    fname_output = sys.argv[3]

    try:
        file_itcont = open(fname_itcont, 'r')
        file_output = open(fname_output, 'w')

        with open(fname_percentile) as file_percentile:
            try:
                percentile_str = file_percentile.readline()
                percentile = int(percentile_str)
            except ValueError:
                print("Malformed percentile value:", percentile_str)
                exit(0)

    except IOError as e:
        print("IOError Exception:", e)
        exit(0)

    reader = csv.reader(file_itcont, delimiter='|')
    writer = csv.writer(file_output, delimiter='|')

    donors_all = set()                  # set for all donors_id
    recipients_all = defaultdict(list)  # dict {recipient_id: [donations]}

    parser = parser.LineParser()

    for line in reader:
        if not parser.parse(line):
            continue

        recipient = parser.recipient
        donor_name = parser.donor_name
        zip_code = parser.zip_code
        year = parser.year
        amount = parser.amount

        # create a donor_id
        donor_id = donorID(donor_name, zip_code)

        if donor_id in donors_all:
            # this is a repeat donor

            # append the amount to list of donations for the recipient
            recipient_id = recipientID(recipient, zip_code, year)
            recipients_all[recipient_id].append(amount)

            # find the donation by percentile
            n_donations = len(recipients_all[recipient_id])
            index = int(math.ceil(n_donations * percentile / 100.) - 1)
            if index < 0:
                index = 0               # if pecentile == 0
            if index >= n_donations:
                index = n_donations - 1 # if percentile > 100

            recipients_all[recipient_id].sort() # sort in increasing order
            percentile_amount = recipients_all[recipient_id][index]
            ipercentile_amount = int(percentile_amount + 0.50)
            
            amount_sum = sum(recipients_all[recipient_id])
            iamount_sum = int(amount_sum)
            writer.writerow((recipient, zip_code, year, ipercentile_amount,
                             iamount_sum, len(recipients_all[recipient_id])))
        else:
            # this is a first time donor
            donors_all.add(donor_id)    # register the donor: place into set

    file_itcont.close()
    file_output.close()

    # show nlines_max lines from the output file
    nlines_max = 10
    with open(fname_output) as file_output:
        reader = csv.reader(file_output, delimiter='|')
        for nlines, line in enumerate(reader):
            print(line)
            if nlines == nlines_max:
                break
