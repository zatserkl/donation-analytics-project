# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 8, 2018

import parser

import sys
import csv
import math

from collections import defaultdict


def donorID(name, zip_code):
    """User is identified by its name and zip_code only"""
    return (name, zip_code)

def recipientID(recipient, zip_code, year):
    """recipient from zip_code at year"""
    return (recipient, zip_code, year)


def read_file(fname):
    fields_str = "CMTE_ID AMNDT_IND RPT_TP TRANSACTION_PGI IMAGE_NUM " \
            "TRANSACTION_TP ENTITY_TP NAME CITY STATE ZIP_CODE EMPLOYER " \
            "OCCUPATION TRANSACTION_DT TRANSACTION_AMT OTHER_ID TRAN_ID " \
            "FILE_NUM MEMO_CD MEMO_TEXT SUB_ID"

    print(fields_str)

    fields = fields_str.split()
    print("fields =", fields)
    # print("fields[10] =", fields[10])
    print()

    # with open(fname) as file:


if __name__ == "__main__":

    for i, fname in enumerate(sys.argv):
        print(i, fname)

    if len(sys.argv) < 3:
        print("Usage: python", __file__, "input_file percentile_file output_file")
        exit(0)

    fname_itcont = sys.argv[1]
    fname_percentile = sys.argv[2]
    fname_output = sys.argv[3]

    print(fname_itcont, fname_percentile, fname_output)

    try:
        file_itcont = open(fname_itcont, 'r')
        file_output = open(fname_output, 'w')

        with open(fname_percentile) as file_percentile:
            percentile = int(file_percentile.readline())

    except IOError as e:
        print("IOError Exception:", e)
        exit(0)

    reader = csv.reader(file_itcont, delimiter='|')
    writer = csv.writer(file_output, delimiter='|')

    donors_all = set()                  # all donors_id
    recipients_all = defaultdict(list)  # {recipient_id: [contributions]}

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
            # this is a repeat donor: process the donation
            recipient_id = recipientID(recipient, zip_code, year)
            recipients_all[recipient_id].append(amount)

            # find the donation by percentile
            n_donations = len(recipients_all[recipient_id])
            index = math.ceil(n_donations * percentile / 100) - 1

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

    with open(fname_output) as file_output:
        reader = csv.reader(file_output, delimiter='|')
        nlines_max = 10
        for nlines, line in enumerate(reader):
            print(line)
            if nlines == nlines_max:
                break

    # input("<CR> to quit ")
