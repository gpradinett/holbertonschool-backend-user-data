#!/usr/bin/env python3

import re

def filter_datum(fields, redaction, message, separator):
    pattern = f'(?:{separator})({fields})(?:{separator})'
    return re.sub(pattern, redaction, message)
