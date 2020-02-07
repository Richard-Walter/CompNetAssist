""" This program is assists in survey CompNet adjustments.

Written by Richard Walter 2020
"""

import re

"""
.       - Any Character Except New Line
\d      - Digit (0-9)
\D      - Not a Digit (0-9)
\w      - Word Character (a-z, A-Z, 0-9, _)
\W      - Not a Word Character
\s      - Whitespace (space, tab, newline)
\S      - Not Whitespace (space, tab, newline)

\b      - Word Boundary
\B      - Not a Word Boundary
^       - Beginning of a String
$       - End of a String

[]      - Matches Characters in brackets (Character sets)
[^ ]    - Matches Characters NOT in brackets
|       - Either Or
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)

"""

# use code below to search for easting and northings in a text file

pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
mypattern_easting = re.compile(r'\b28\d{4}\.\d{4}')
mypattern_northing = re.compile(r'\b62\d{5}\.\d{4}')
mypattern_easting_and_northing = re.compile(r'\b(28|62)\d{4,5}\.\d{4}') # Need to use iterable on this pattern


# 1 285968.9510 6215310.3810 0.010 0.010 "STN03"

try:
    with open('data.txt', 'r') as f:

        for line in f:
            match = mypattern_northing.search(line)
            print(match.group())

except Exception as ex:
    print(ex)

# use this code to read in a file and replace text.

original_file_path = 'Files\\AA9 ARTC 030220.FIX'

try:
    with open(original_file_path, 'r') as f_orig:

        original_contents = f_orig.readlines()
        updated_contents = ""
        old_easting = '500000.000'
        new_easting = '111111.111'

        old_northing = '10000000.000'
        new_northing = '22222222.222'

        print (original_contents)

        for line in original_contents:

            # print(line)

            updated_line_easting = line.replace(old_easting, new_easting, 1)
            updated_line_easting_and_northing = updated_line_easting.replace(old_northing, new_northing)

            updated_contents += updated_line_easting_and_northing

            print(updated_line_easting_and_northing)

        print(updated_contents)

        with open(original_file_path, 'w') as f_update:

            f_update.write(updated_contents)

except Exception as ex:
    print(ex)