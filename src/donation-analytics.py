# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 8, 2018

import sys
import csv
import numpy as np

from collections import defaultdict, Counter
from numpy import nan as NA

class DonorContribution:
    def __init__(self, committee, zip_code, amount):
        self.committee = committee
        self.zip_code = zip_code
        self.amount = amount

    def __repr__(self):
        return committee + " " + str(zip_code) + " " + str(amount)

    def __str__(self):
        return committee + " " + str(zip_code) + " " + str(amount)

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
    nlines = 0
    for line in reader:
        if len(line[10]) == 0:
            # print("-- empty zip_code in line", nlines)
            nlines_empty_zip_code.append(nlines)
        if nlines < nlines_max:
            pass
            # print(line)

            # convert zip_code to int

            try:
                # zip_code_str = line[10][:5]
                # zip_code = int(zip_code_str)
                zip_code = int(line[10][:5])
            except ValueError as e:
                # print("--- Error castling zip_code as int for", zip_code_str)
                print("--- Error castling zip_code as int for", line[10])
                continue

            # good ZIP_CODE here

            # print(line[10], "zip_code =", zip_code)
        
        # process the line
        print("zip_code =", zip_code)

        name = line[7]
        committee = line[0]
        # zip_code = line[10]
        amount = line[14]
        
        donor = DonorContribution(committee, zip_code, amount)
        # print(donor)

        if name in donors_repeat:
            print("  -- append to key", name)
            donors_repeat[name].append(donor)
        else:
            if name in donors_all:
                print("  ++ copy from donors_all name =", name)
                donors_repeat[name].append(donors_all[name])
                donors_repeat[name].append(donor)
            else:
                print("  .. add name", name, "to donors_all")
                donors_all[name] = donor

        nlines += 1

    print("read", nlines, "lines")
    print("found", len(nlines_empty_zip_code), "lines with empty zip code")
    print("nlines_empty_zip_code[:10]:", nlines_empty_zip_code[:10])

    print("donors_all:\n", donors_all)
    print("donors_repeat:\n", donors_repeat)

    # input("<CR> to quit ")
