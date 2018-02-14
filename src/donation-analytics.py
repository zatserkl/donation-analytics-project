# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 11, 2018

from __future__ import print_function       # to run this code under python27
import csv
import sys

import parser
import processor


def donation_analytics(reader, percentile, writer):
    """
    Creates instances of line parser and donation processor.
    Can be extended for the analysis of data stored in the
    containers of the DonationProcessor class after the loop.
    """

    lineParser = parser.LineParser()
    donationProcessor = processor.DonationProcessor()

    for line in reader:
        if not lineParser.parse(line):
            continue

        # process donation data stored in lineParser
        donationProcessor.process_donation(lineParser, percentile, writer)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python", __file__,
              "input_file percentile_file output_file")
        exit(0)

    fname_itcont = sys.argv[1]
    fname_percentile = sys.argv[2]
    fname_output = sys.argv[3]

    file_itcont = None
    file_output = None
    percentile = 0
    try:
        file_itcont = open(fname_itcont, 'r')
        file_output = open(fname_output, 'w')

        with open(fname_percentile) as file_percentile:
            percentile_str = ""
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

    donation_analytics(reader, percentile, writer)

    file_itcont.close()
    file_output.close()
