# Table of Contents
1. [Python version](README.md#Pyhon-version)
2. [Description of the method](README.md#Description-of-the-method)
2. [Discussion](README.md#Discussion)
3. [Remarks on the code implementation](README.md#Remarks-on-the-code-implementation)
                
# Python version

The code was developed with Python 3.6.3:

        donation-analytics-project$ python --version
        Python 3.6.3 :: Anaconda custom (64-bit)

The code seems to work also with Python 2.7.14 (Anaconda) and Python 2.7.10 (macOS High Sierra).

The code imports standard modules:

        from __future__ import print_function # to run this code under python27
        from collections import defaultdict
        import csv
        import math
        import sys

# Description of the method

Technically the code fills up a dictionary:

        key:    a tuple of the recipient's ID (alpha-numeric code), zip_code of the donors, and year

        value:  a list of contributions that come from repeated donors with the key's zip_code

The code uses contributions from the repeated donors only. To mark the donor as a repeat donor, the code places an ID of each new donor (a tuple with the donor name and donor zip\_code) into Python's set. 

Note: Following the procedure in the code challenge documentation we ignore the first contribution of each donor (because she/he was not a repeated donor at that time).

After every update of the dictionary value (append the current contribution to the list of contributions), the code calculates a sum of the contributions, finds a contribution for the given percentile and streams the line into the output file.

# Discussion

A brief investigation shows that most contributions come from the repeat donors.

In the first 700K lines of indiv18/itcont.txt the total number of donations from repeat donors is 417K out of total 550K personal contributions.
Also, the number of all donors is 237K while the number of repeat donors is smaller at 103K.

Therefore, the code searches the dictionary with repeated donors first. Then if the search over the dictionary of repeat donors fails, it runs search over the set with all donors. It is worth mentioning that both Python's set and dictionary are very efficient for the search with the time complexity of O(1).

# Remarks on the code implementation

The variables for the column numbers in the module parser.py are made in upper case intentionally because they were not typed but copied/pasted from the documentation (to avoid typos).

The package consists of three modules.

### parser.py
Contains class LineParser that carries out the basic checks on the current line and extracts data of interest

### processor.py
Contains class DonationProcessor that processes clean data from the current line provided by LineParser. It also contains general purpose functions that can be used for the data analysis in the calling routine.

The containers of the DonationProcessor can be analyzed after finishing processing of the input file.

### donation-analytics.py
The function donation\_analytics() creates instances of the LineParser and DonationProcessor.

This function can be extended for analysis of the data stored in the DonationProcessor containers.
