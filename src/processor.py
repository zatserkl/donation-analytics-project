# Andriy Zatserklyaniy <zatserkl@gmail.com> Feb 13, 2018

from __future__ import print_function       # to run this code under python27
from collections import defaultdict
import math


# General purpose function to provide value in standard form


def get_donor_id(name, zip_code):
    """User is identified by its name and zip_code only"""
    return name, zip_code


def get_recipient_id(recipient, zip_code, year):
    """recipient from zip_code at year"""
    return recipient, zip_code, year


def dollars_cents(amount):
    """
    Returns a string
    100     for float numbers 100, 100. or 100.0
    100.10  for the float number 100.10
    """
    if amount > int(amount):
        return "{0:.2f}".format(amount)
    else:
        return "{0:.0f}".format(amount)


class DonationProcessor:
    """ Processes data extracted by LineParser from the current line.
    """

    def __init__(self):
        """
        Books two main containers:
        self.donors_all is a set with donor_id for all donors
        self.recipients_all is a dictionary {recipient_id: [donations]}
        """
        self.donors_all = set()                  # set for all donors_id
        self.recipients_all = defaultdict(list)  # {recipient_id: [donations]}

    def process_donation(self, lineParser, percentile, writer):
        """
        Takes values from the lineParser and processes the donation
        from the current line. Writes output file if needed.
        """

        recipient = lineParser.recipient
        donor_name = lineParser.donor_name
        zip_code = lineParser.zip_code
        year = lineParser.year
        amount = lineParser.amount

        # create a donor_id
        donor_id = get_donor_id(donor_name, zip_code)

        if donor_id in self.donors_all:
            # this is a repeat donor

            # append the amount to list of donations for the recipient
            recipient_id = get_recipient_id(recipient, zip_code, year)
            self.recipients_all[recipient_id].append(amount)

            # find the donation by percentile
            n_donations = len(self.recipients_all[recipient_id])
            index = int(math.ceil(n_donations * percentile / 100.) - 1)
            if index < 0:
                index = 0                               # if percentile == 0
                if index >= n_donations:
                    index = n_donations - 1             # if percentile > 100

            self.recipients_all[recipient_id].sort()    # increasing order
            percentile_amount = self.recipients_all[recipient_id][index]
            percentile_amount_str = dollars_cents(percentile_amount)

            amount_sum = sum(self.recipients_all[recipient_id])
            amount_sum_str = dollars_cents(amount_sum)
            writer.writerow((recipient, zip_code, year,
                             percentile_amount_str, amount_sum_str,
                             len(self.recipients_all[recipient_id])))
        else:
            # this is a first time donor
            self.donors_all.add(donor_id)   # register donor: place id into set
