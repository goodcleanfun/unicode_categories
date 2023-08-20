"""
word_breaks.py

This script is used to automatically build ranges of unicode characters
from the unicode spec's word break properties. These ranges help us
build a tokenizer that does the right thing in every language with regard
to word segmentation.
"""

import csv
import io
import requests
from collections import defaultdict
import re
from unicode_regexes import regex_chars_to_ranges

UNICODE_DATA_URL = "https://unicode.org/Public/UNIDATA/UnicodeData.txt"


def fetch_unicode_categories():
    unicode_cats = {}
    response = requests.get(UNICODE_DATA_URL)
    reader = csv.reader(io.StringIO(response.text), delimiter=';')
    for row in reader:
        ch = row[0]
        cat = row[2]
        unicode_cats.setdefault(cat, [])
        unicode_cats[cat].append(ch)
    return unicode_cats

readable_names = {
    'Cc': 'control_chars',
    'Cf': 'other_format_chars',
    'Co': 'other_private_use_chars',
    'Cs': 'other_surrogate_chars',

    'Ll': 'letter_lower_chars',
    'Lm': 'letter_modifier_chars',
    'Lo': 'letter_other_chars',
    'Lt': 'letter_title_chars',
    'Lu': 'letter_upper_chars',
    'Mc': 'mark_spacing_combining_chars',
    'Me': 'mark_enclosing_chars',
    'Mn': 'mark_nonspacing_chars',
    'Nd': 'number_or_digit_chars',
    'Nl': 'number_letter_chars',
    'No': 'number_other_chars',
    'Pc': 'punct_connector_chars',
    'Pd': 'punct_dash_chars',
    'Pe': 'punct_close_chars',
    'Pf': 'punct_final_quote_chars',
    'Pi': 'punct_initial_quote_chars',
    'Po': 'punct_other_chars',
    'Ps': 'punct_open_chars',
    'Sc': 'currency_symbol_chars',
    'Sk': 'symbol_modifier_chars',
    'Sm': 'symbol_math_chars',
    'So': 'symbol_other_chars',
    'Zl': 'separator_line_chars',
    'Zp': 'separator_paragraph_chars',
    'Zs': 'space',
}


def main():
    """Insert these lines into scanner.re"""
    unicode_cats = fetch_unicode_categories()
    if unicode_cats:
        prev = None
        for cat in sorted(unicode_cats):
            if prev and prev[0] != cat[0]:
                print()
            chars = unicode_cats[cat]
            name = readable_names[cat]
            char_ranges = regex_chars_to_ranges(chars)
            print(f"{name} = [{''.join(char_ranges)}]")
            prev = cat

if __name__ == "__main__":
    main()
