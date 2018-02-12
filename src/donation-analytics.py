# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 8, 2018

import sys
import csv
import numpy as np

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

    try:
        file_itcont = open(fname_itcont, 'r')

    except IOError as e:
        print("IOError Exception:", e)
        exit(0)

    reader = csv.reader(file_itcont, delimiter='|')

    donors_all = defaultdict(list)      # all donors
    donors_repeat = defaultdict(list)   # repeat donors

    nlines_empty_zip_code = []

    nlines_max = 10

    valid_donations = 0

    for nlines, line in enumerate(reader):

        # process the ZIP_CODE

        if len(line[10]) == 0:
            # print("-- empty zip_code in line", nlines)
            nlines_empty_zip_code.append(nlines)

        if nlines < nlines_max:
            pass
            # print(line)

            # convert zip_code to int

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

        name = line[7]
        recipient = line[0]
        donor = DonorContribution(recipient, zip_code, amount, year)
        # print(donor)

        if name in donors_repeat:
            # print("  -- append to key", name)
            donors_repeat[name].append(donor)
        else:
            if name in donors_all:
                # print("  ++ copy from donors_all name =", name)
                donors_repeat[name].append(donors_all[name])
                # print("     -- and append the current entry for name", name)
                donors_repeat[name].append(donor)
            else:
                # print("  .. add name", name, "to donors_all")
                donors_all[name] = donor

        nlines += 1

    print("read", nlines, "lines")
    print("found", len(nlines_empty_zip_code), "lines with empty zip code")
    print("nlines_empty_zip_code[:10]:", nlines_empty_zip_code[:10])

    # print("donors_all:\n", donors_all)
    # print("donors_repeat:\n", donors_repeat)

    print("\nThe first donors:")
    for i, donor in enumerate(donors_repeat.items()):
        if i > 10:
            break
        # print(donor[0], "#donors:", len(donor[1]), "list:", donor[1])
        print(donor[0], "# of donations:", len(donor[1]))

    total_repeat = sum([len(x) for x in donors_repeat.values()])
    print("total_repeat =", total_repeat, "out of total", valid_donations)
    print("len(donors_repeat.keys()) =", len(donors_repeat.keys()),
          "len(donors_all.keys()) =", len(donors_all.keys()))

    # input("<CR> to quit ")
