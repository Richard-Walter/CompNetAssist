""" This program is assists in survey CompNet adjustments.

Written by Richard Walter 2020
"""

import re


'''
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

[]      - Matches Characters in brackets
[^ ]    - Matches Characters NOT in brackets
|       - Either Or
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)


#### Sample Regexs ####

[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+


'''

text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890
Ha HaHa
MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )
coreyms.com
321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234
Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
'''


pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
mypattern_easting = re.compile(r'\b28\d\d\d\d\.\d\d\d\d')
mypattern_northing = re.compile(r'\b62\d\d\d\d\d\.\d\d\d\d')

# matches = mypattern_northing.finditer(compnet_to_search_CRD)
#
#
# for match in matches:
#
#     print(match.span())
#     print(match.group())


try:
    with open('data.txt', 'r') as f:

        for line in f:

            match = mypattern_easting.search(line)
            print(match.group())

except Exception as ex:
    print(ex)