# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 8, 2018

import sys
import csv
import numpy as np
import math

from collections import defaultdict, Counter
from numpy import nan as NA

class DonorContribution:
    def __init__(self, recipient, zip_code, amount, year):
        self.recipient = recipient
        self.zip_code = zip_code
        self.amount = amount
        self.year = year

    def __repr__(self):
        return recipient + " " + zip_code + " " + str(amount) + " " + str(year)

    def __str__(self):
        return recipient + " " + zip_code + " " + str(amount) + " " + str(year)

class Donor:
    def __init__(self, zip_code, amount, year):
        self.zip_code = zip_code
        self.amount = amount
        self.year = year

    @staticmethod
    def id(name, zip_code):
        """User is identified by its name and zip_code only"""
        return (name, zip_code)

    def __repr__(self):
        return recipient + " " + zip_code + " " + str(amount) + " " + str(year)

    def __str__(self):
        return recipient + " " + zip_code + " " + str(amount) + " " + str(year)

def donorID(name, zip_code):
    """User is identified by its name and zip_code only"""
    return (name, zip_code)

def recipientID(recipient, zip_code, year):
    """recipient from zip_code at year"""
    return (recipient, zip_code, year)


class RecipientID:
    @staticmethod
    def id(recipient, zip_code, year):
        return (recipient, zip_code, year)


class Recipient:
    def __init__(self, recipient, zip_code, year, amount):
        pass
        id = get_id(recipient, zip_code, year)
        self.ostream[id].append(amount)

        # calculate percentile and stream into output file
        pvalue = percentile_value(percentile, amounts)
        writer = csv.writer(sys.stdout)
        writer.write(self.ostream[id], pvalue, sum(amounts), delimitor='|')

    @staticmethod
    def id(recipient, zip_code, year):
        """Id for contribution for recipient from zip_code at year"""
        return (recipient, zip_code, year)

    def percentile_value(self, percentile, amounts):
        n = len(amounts)
        index = math.ceil(n * percentile / 100)
        return amounts[index]

# class Reader:


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

    if len(sys.argv) < 2:
        print("Usage: python", __file__, "input_file output_file")
        exit(0)

    fname_itcont = sys.argv[1]

    percentile = 30
    print("\nhardcoded percentile = ", percentile, "\n")

    try:
        file_itcont = open(fname_itcont, 'r')

    except IOError as e:
        print("IOError Exception:", e)
        exit(0)

    reader = csv.reader(file_itcont, delimiter='|')

    writer = csv.writer(sys.stdout, delimiter='|')

    donors_all = defaultdict(list)      # all donors
    donors_repeat = defaultdict(list)   # repeat donors
    ostream = defaultdict(list)         # dict to stream into output file

    donors_all_set = set()              # fast container to search
    recipients_all = defaultdict(list)  # {recipient_id: [contributions]}

    nlines_empty_zip_code = []

    nlines_max = 10

    valid_donations = 0

    for nlines, line in enumerate(reader):

        if len(line[15]) > 0:
            continue            # this is not a person contribution

        # for information purpose only
        if len(line[10]) == 0:
            # print("-- empty zip_code in line", nlines)
            nlines_empty_zip_code.append(nlines)

        if nlines < nlines_max:
            pass
            # print(line)

        recipient = line[0]
        if len(recipient) == 0:
            continue
        
        donor_name = line[7]
        if len(donor_name) == 0:
            continue

        zip_code = line[10][:5]
        if len(zip_code) < 5:
            continue

        # process the year: convert to int
        try:
            year = int(line[13][4:])
        except ValueError as e:
            # print("--- Error castling year as int for", line[13])
            continue

        # process the amount: convert to float
        try:
            amount = int(line[14])
        except ValueError as e:
            # print("--- Error castling amount as float for", line[14])
            continue
        
        valid_donations += 1

        #
        # the donation is valid, process it
        #

        # create a donor_id
        donor_id = donorID(donor_name, zip_code)
        # print("--- donor_id:", donor_id)
        if donor_id in donors_all_set:
            # process the donation
            pass
            recipient_id = recipientID(recipient, zip_code, year)
            # print("+++ recipient_id:", recipient_id)
            recipients_all[recipient_id].append(amount)
            # output_line
            # percentile calculation
            n = len(recipients_all[recipient_id])
            index = math.ceil(n * percentile / 100) - 1
            # print("index =", index)
            recipients_all[recipient_id].sort() # sort in increasing order
            percent = recipients_all[recipient_id][index]
            # print("percent =", percent)
            
            writer.writerow((recipient, zip_code, year, percent, amount,
                            len(recipients_all[recipient_id])))
        else:
            donors_all_set.add(donor_id)    # register the donor

        ################## end of processing ##################

        nlines += 1

    print("read", nlines, "lines")
    print("found", len(nlines_empty_zip_code), "lines with empty zip code")
    print("nlines_empty_zip_code[:10]:", nlines_empty_zip_code[:10])

    print("\nNew Algoritm\n")

    print(donors_all_set)

    # input("<CR> to quit ")
