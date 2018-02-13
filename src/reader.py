import csv
import math

class reader:
    def __init__(self, file_input):
        fields_str = "CMTE_ID AMNDT_IND RPT_TP TRANSACTION_PGI IMAGE_NUM " \
            "TRANSACTION_TP ENTITY_TP NAME CITY STATE ZIP_CODE EMPLOYER " \
            "OCCUPATION TRANSACTION_DT TRANSACTION_AMT OTHER_ID TRAN_ID " \
            "FILE_NUM MEMO_CD MEMO_TEXT SUB_ID"

        iname = 0
        cell_id = {}
        for name in list(field_str):
            cell_id[name] = iname
            iname += 1

        print(cell_id)
