import csv
import math

class LineParser:
    """ Parses line and provides basic checks.
    """

    def __init__(self):
        self.debug = False

    def clear(self):
        """ Clear the data field before read of the line
        """
        self.recipient = ""
        self.donor_name = ""
        self.zip_code = ""      # use as string to keep leading zeros
        self.year = ""
        self.amount = 0.

    def parse(self, line):
        """ Takes the next line from the input file, assign variables and
            carries out basic checks.
            Returns True for the valid line.
        """

        self.clear()

        # set values to the local variables for the columns indices
        CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, \
        TRANSACTION_TP, ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, \
        OCCUPATION, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, TRAN_ID, \
        FILE_NUM, MEMO_CD, MEMO_TEXT, SUB_ID = range(21)

        if len(line[OTHER_ID]) > 0:
            if self.debug:
                print("not empty OTHER_ID:", line[OTHER_ID])
            return False    # this is not a contribution from individual

        if len(line[TRANSACTION_DT]) < 8:
            if self.debug:
                print("empty TRANSACTION_DT")
            return False

        if len(line[NAME]) == 0:
            if self.debug:
                print("empty NAME")
            return False    # empty name

        if len(line[CMTE_ID]) == 0:
            if self.debug:
                print("empty CMTE_ID")
            return False    # empty recipient id

        if len(line[TRANSACTION_AMT]) == 0:
            if self.debug:
                print("empty TRANSACTION_AMT")
            return False    # empty amount field

        if len(line[ZIP_CODE]) < 5:
            if self.debug:
                print("Malformed ZIP_CODE")
            return False

        self.recipient = line[CMTE_ID]
        self.donor_name = line[NAME]
        self.zip_code = line[ZIP_CODE]

        try:
            self.amount = float(line[TRANSACTION_AMT])
        except ValueError as e:
            if self.debug:
                print("Malformed contribution amount:", e)
            return False
        if self.amount <= 0:
            return False

        try:
            # convert time to make sure that the date is fine
            month = int(line[TRANSACTION_DT][:2])
            day = int(line[TRANSACTION_DT][2:4])
            year = int(line[TRANSACTION_DT][4:])
        except ValueError as e:
            if self.debug:
                print("Malformed date:", e)
            return False

        if year < 1900 or year > 2100:
            if self.debug:
                print("Malformed date")
            return False
        if month < 1 or month > 12:
            if self.debug:
                print("Malformed date")
            return False
        if day < 1 or day > 31:
            if self.debug:
                print("Malformed date")
            return False

        return True
