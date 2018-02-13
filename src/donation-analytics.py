# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 8, 2018

import reader

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

    reader = reader.Reader(file_itcont)
    reader.get_line()
    print("reader.line_number:", reader.line_number)
    reader.get_line()
    print("reader.line_number:", reader.line_number)

    reader = csv.reader(file_itcont, delimiter='|')
    writer = csv.writer(file_output, delimiter='|')

    donors_all = set()                  # all donors_id
    recipients_all = defaultdict(list)  # {recipient_id: [contributions]}

    nlines_empty_zip_code = []

    valid_donations = 0

    nlines = 0                          # make the name nlines global

    for nlines, line in enumerate(reader):

        if len(line[15]) > 0:
            continue            # this is not a person contribution

        # for information purpose only
        if len(line[10]) == 0:
            nlines_empty_zip_code.append(nlines)

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
        if donor_id in donors_all:
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
            donors_all.add(donor_id)    # register the donor

        ################## end of processing ##################

    # print("read", nlines, "lines")
    # print("found", len(nlines_empty_zip_code), "lines with empty zip code")
    # print("nlines_empty_zip_code[:10]:", nlines_empty_zip_code[:10])

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
