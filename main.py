"""
This program is assists in survey CompNet adjustments.

Written by Richard Walter 2020
"""

import re


class FixedFile:

    def __init__(self, fixed_file_path):

        self.fixed_file_path = fixed_file_path
        self.file_contents = None
        self.updated_file_contents = ""
        self.station_list = []

        with open(fixed_file_path, 'r') as f_orig:
            self.file_contents = f_orig.readlines()

    # returns a list of stations from the fixed file that need need to be updated
    def get_station_list(self):

        # Line number is at the start of a string and contains digits followed by whiespace
        re_pattern = re.compile(r'"\w+"')

        for line in self.file_contents:
            match = re_pattern.search(line)

            # strip of quotation marks and add to station list
            self.station_list.append(match.group()[1:-1])

        return self.station_list

    def get_line_number(self, station):

        # Line number is at the start of a line
        re_pattern = re.compile(r'^\d+\s')
        line_number = "???"

        for line in self.file_contents:

            if station in line:
                match = re_pattern.search(line)
                line_number = match.group()
                break

        return line_number

    def update(self, coordinate_contents):

        re_pattern_easting = re.compile(r'\b28\d{4}\.\d{4}')
        re_pattern_northing = re.compile(r'\b62\d{5}\.\d{4}')
        updated_file_dictionary = {}

        self.station_list = self.get_station_list()

        # check each line of the coordinate contents to see if it contains a matching station.
        for coordinate_contents_line in coordinate_contents:
            for station in self.station_list:
                if station in coordinate_contents_line:
                    # grab easting and northing for this station
                    easting_match = re_pattern_easting.search(coordinate_contents_line)
                    northing_match = re_pattern_northing.search(coordinate_contents_line)

                    # create a dictionary so that we can later order by line number and write out to file
                    updated_file_dictionary[int(self.get_line_number(station))] = easting_match.group() + '  ' + \
                                                                                  northing_match.group() + ' ' + '"'\
                                                                                  + station +'"\n'
                    break

        # order updated file contents by line number
        for line_number in sorted(updated_file_dictionary):
            update_file_line = str(line_number) + ' ' + updated_file_dictionary[line_number]
            self.updated_file_contents += update_file_line

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


def main():

    # Create GUI - see GSI Query

    # temporary file paths - replace by user chosen within GUI??
    coordinate_file_path = 'Files\\AA9 ARTC_130120.CRD'
    fixed_file_path = 'Files\\AA9 ARTC 030220.FIX'

    try:

        # open up fixed file & update the fixed file's easting/northings from the coordinate file
        fixed_file = FixedFile(fixed_file_path)
        coordinate_file = CoordinateFile(coordinate_file_path)
        fixed_file.update(coordinate_file.file_contents)

    except Exception as ex:
        print(ex, type(ex))

    else:
        print("SUCCESS")


if __name__ == '__main__':
    main()

