"""

This program assists in survey CompNet adjustments.

Written by Richard Walter 2020

"""

import re


class FixedFile:

    def __init__(self, fixed_file_path):

        self.fixed_file_path = fixed_file_path
        self.fixed_file_contents = None
        self.station_list = []
        self.updated_file_contents = ""

        with open(fixed_file_path, 'r') as f_orig:
            self.fixed_file_contents = f_orig.readlines()

    @staticmethod
    def get_station(line):

        station = "UNKNOWN"

        # Line number is at the start of a string and contains digits followed by whiespace
        re_pattern = re.compile(r'"\w+"')
        match = re_pattern.search(line)

        # strip of quotation marks and add to station list
        if match is not None:
            station = match.group()[1:-1]

        return station

    @staticmethod
    def get_line_number(line):

        line_number = "???"

        # Line number is at the start of a line
        re_pattern = re.compile(r'^\d+\s')

        match = re_pattern.search(line)

        if match:
            line_number = match.group().strip()

        return line_number

    def update(self, coordinate_file):

        for line in self.fixed_file_contents:

            # Get coordinates for this station if exists in the coordinate file
            station = self.get_station(line)

            coordinate_dict = coordinate_file.get_coordinates(station)

            # update fixed_file coordinate if a match was found
            if coordinate_dict:
                easting = coordinate_dict['Eastings']
                northing = coordinate_dict['Northings']

                updated_line = self.get_line_number(line) + ' ' + easting + '  ' + northing + ' "' + station + '"\n'
                self.updated_file_contents += updated_line

            else:
                self.updated_file_contents += line

        print(self.updated_file_contents)

        # update fixed file with updated contents
        with open(self.fixed_file_path, 'w') as f_update:
            f_update.write(self.updated_file_contents)


class CoordinateFile:

    def __init__(self, coordinate_file_path):

        self.file_contents = None

        try:
            with open(coordinate_file_path, 'r') as f_orig:

                self.file_contents = f_orig.readlines()

        except Exception as ex:
            print(ex, type(ex))

        else:
            pass

    def get_coordinates(self, station):

        re_pattern_easting = re.compile(r'\b28\d{4}\.\d{4}')
        re_pattern_northing = re.compile(r'\b62\d{5}\.\d{4}')

        coordinate_dict = {}

        # check each line of the coordinate contents to see if it contains a matching station.
        for coordinate_contents_line in self.file_contents:
            if station in coordinate_contents_line:
                # grab easting and northing for this station
                easting_match = re_pattern_easting.search(coordinate_contents_line)
                northing_match = re_pattern_northing.search(coordinate_contents_line)
                coordinate_dict['Eastings'] = easting_match.group()
                coordinate_dict['Northings'] = northing_match.group()

                break

        return coordinate_dict


def main():
    # Create GUI - see GSI Query

    # temporary file paths - replace by user chosen within GUI??
    coordinate_file_path = 'Files\\AA9 ARTC_130120.CRD'
    # coordinate_file_path = 'Files\\AA9 ARTC_130120.STD'

    fixed_file_path = 'Files\\AA9 ARTC 030220.FIX'

    try:

        # open up fixed file & update the fixed file's easting/northings from the coordinate file
        fixed_file = FixedFile(fixed_file_path)
        coordinate_file = CoordinateFile(coordinate_file_path)
        fixed_file.update(coordinate_file)

    except Exception as ex:
        print(ex, type(ex))

    else:
        print("SUCCESS")


if __name__ == '__main__':
    main()
