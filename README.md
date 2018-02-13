# Table of Contents
1. [Python vesion](README.md#Pyhon-version)
2. [Description of the method](README.md#Description-of-the-method)
2. [Discussion](README.md#Discussion)
                
# Python vesion

I developed this code under Python 3.6.3:

donation-analytics-project$ python --version

Python 3.6.3 :: Anaconda custom (64-bit)

The code seems to be runnable also under Python 2.7.14 (Anaconda) and Python 2.7.10 (macOS High Sierra).

# Description of the method

Technically the code fills up a dictionary:

        key:    a tuple of the recipient's ID (alpha-numeric code), zip_code of the donors, and year
        
        value:  a list of contributions

The code uses contributions from the repeated donors only. To mark the donor as a repeat donor, the code places an ID of each new donor (a tuple with the donor name and donor zip\_code) into a Python set. 

After every update of the dictionary value (append the current contribution to the list of contributions), the code calculates a sum of the contributions, finds a contribution for the given percentile and streams the line into the output file.

# Discussion

A brief investigation shows that the most contributions come from the repeat donors.

In the first 700K lines of indiv18/itcont.txt the total number of donations from repeat donors is 417K out of total 550K personal contributions.

Also, the number of all donors is 237K while the number of repeat donors is smaller at 103K.

Therefore, the code search the dictionary with repeated donors first and search the set with all the donor IDs if the search in dictionary of the repeat donors failed. It worth mentioning that both Python's set and dictionary are very efficient for the search with the time complexity of O(1).
