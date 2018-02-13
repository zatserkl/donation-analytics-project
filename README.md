# Table of Contents
1. [Draft](README.md#Draft)
2. [Python vesion](README.md#Pyhon-version)
3. [Introduction](README.md#introduction)
4. [Challenge summary](README.md#challenge-summary)
5. [Details of challenge](README.md#details-of-challenge)
6. [Input files](README.md#input-files)
7. [Output file](README.md#output-file)
8. [Percentile computation](README.md#percentile-computation)
9. [Example](README.md#example)
10. [Writing clean, scalable and well-tested code](README.md#writing-clean-scalable-and-well-tested-code)
11. [Repo directory structure](README.md#repo-directory-structure)
12. [Testing your directory structure and output format](README.md#testing-your-directory-structure-and-output-format)
13. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
14. [FAQ](README.md#faq)
                
# Python vesion

I developed this code under Python 3.6.3:

donation-analytics-project$ python --version

Python 3.6.3 :: Anaconda custom (64-bit)

The code seems to be runnable also under Python 2.7.14 (Anaconda) and Python 2.7.10 (macOS High Sierra).

# Draft

Technically the code fills up a dictionary:

        key:    a tuple of the recipient code, zip_code of the donors, and year
        
        value:  a list of contributions

The code takes data from the repeated donors. To mark the donor as a repeat donor, the code places an ID of each new donor (a tuple with the donor name and donor zip\_code) into a Python set. 

After every update of the dictionary value (append the current contribution to the list of contributions), the code calculates a sum of the contributions, finds a contribution for the given percentile and streams the line into the output file.

Technically the code fills up a dictionary with a key that is a tuple of the recipient code, zip\_code of the donors, and year and a value that is a list of contributions. The code takes data from the repeated donors. To mark the repeat donors, the code places an ID of each new donor (a tuple with the donor name and donor zip\_code) into Python set, so if ID of the donor from the current line is in the set, the donor is a repeat donor. 

A Method to select and other remarks.

The number of repeat donors should be much smaller than the total number of donors (-- investigate this),
so the list of repeat donors should be checked first. 

I used the first 700,000 lines of the indiv18/itcont.txt and found that most of the donations came from the repeat donors:
The total number of donations from repeat donors is 416,570 out of total 549,709 personal contributions.
Also, the number of all donors is 236,294 while the number of repeat donors is smaller at 103,155.

The file input/itcont.txt currently contains the first 500,000 lines of the indiv18/itcont.txt.

From the algorithmic standpoint you have to fill python dictionary with key (recipient, zip\_code, year) using contributions from repeated donors. A Python set is an effective way to keep id of repeated donors id (donor\_name, zip\_code).

Algorithm

Use set as a fast container to keep id of the donors.

1) read current line
2) create a donor\_id
3) find if the donor is a repeated donor (use set)

        if not:

                put the id into set.

                Goto the next line.

        if yes:

                create a recipient_id

                process the recipient_id:

                        add recipient_id into dictionary {recipient_id: list(donation)}

                        calculate percentile

                        write the row into output file
