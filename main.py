"""
This program assists in survey CompNet adjustments:  It can do the following:

1) Allow you to move coordinates automatically over to the fixed file.
2) Compare two CRD files and look for outliers based on a specified tolerance

Written by Richard Walter 2020
"""

import tkFileDialog

from Tkinter import *
import tkMessageBox


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

            coordinate_dict = coordinate_file.get_point_coordinates(station)

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
    re_pattern_easting = re.compile(r'\b28\d{4}\.\d{4}')
    re_pattern_northing = re.compile(r'\b62\d{5}\.\d{4}')
    re_pattern_point_crd = re.compile(r'\b\S+\b')
    re_pattern_point_std = re.compile(r'"\S+"')

    def __init__(self, coordinate_file_path):

        self.file_contents = None
        self.coordinate_dictionary = {}

        try:
            with open(coordinate_file_path, 'r') as f_orig:

                self.file_contents = f_orig.readlines()
                print(self.file_contents)

        except Exception as ex:
            print(ex, type(ex))

        else:
            # remove first 12 lines which contain header text if it is a CRD file
            # remove the first 10 to check 'DESCRIPTION' exists in the header

            if coordinate_file_path[-3:] == 'CRD':
                del self.file_contents[0: 10]
                if 'DESCRIPTION' in self.file_contents[0]:

                    # remove 'description' line plus following blank space'
                    del self.file_contents[0:2]

                else:
                    raise Exception('CRD file Header should contain only 12 rows')

                # build coordinate dictionary STD
                self.build_coordinate_dictionary('CRD')

            else:
                # build coordinate dictionary CRD
                self.build_coordinate_dictionary('STD')

    def get_point_coordinates(self, point):

        if point in self.coordinate_dictionary.keys():
            return self.coordinate_dictionary[point]

    def build_coordinate_dictionary(self, file_type):

        for coordinate_contents_line in self.file_contents:

            point_coordinate_dict = {}
            point_match = None

            try:
                # grab easting and northing for this station
                easting_match = self.re_pattern_easting.search(coordinate_contents_line)
                northing_match = self.re_pattern_northing.search(coordinate_contents_line)

                if file_type == 'CRD':

                    point_match = self.re_pattern_point_crd.search(coordinate_contents_line)

                elif file_type == 'STD':

                    point_match = self.re_pattern_point_std.search(coordinate_contents_line)

                point_coordinate_dict['Eastings'] = easting_match.group()
                point_coordinate_dict['Northings'] = northing_match.group()

                point_name = point_match.group()
                point_name = point_name.replace('"', '')
                print(point_name)

                self.coordinate_dictionary[point_name] = point_coordinate_dict

            except ValueError:
                # probabaly a blank line
                pass

    # @staticmethod
    # def get_point(coordinate_line):
    #
    #     point = ""
    #     re_pattern_point = re.compile(r'\b\S+\b')
    #     point_match = re_pattern_point.search(coordinate_line)
    #
    #     if point_match is not "":
    #         point = point_match.group()
    #     return point


class MainWindow:
    coordinate_file_path = ""
    fixed_file_path = ""
    crd_file_path_1 = ""
    crd_file_path_2 = ""

    def __init__(self, master):

        self.outliers_dict = {}

        # Update Fixed File GUI
        self.update_fixed_file_lbl = Label(master, text='\nUPDATE FIXED FILE\n')
        self.fixed_btn = Button(master, text='(1) Choose Fixed File: ', command=self.get_fixed_file_path)
        self.coord_btn = Button(master, text='(2) Choose Coordinate File: ', command=self.get_coordinate_file_path)
        self.update_btn = Button(master, text='(3) UPDATE FIXED FILE ', command=self.update_fixed_file)
        self.fixed_result_lbl = Label(master, text=' ')
        self.blank_lbl = Label(master, text='')
        self.blank_lbl = Label(master, text='')

        self.update_fixed_file_lbl.pack()
        self.fixed_btn.pack()
        self.coord_btn.pack()
        self.update_btn.pack()
        self.fixed_result_lbl.pack()
        self.blank_lbl.pack()

        # Compare CRD Files GUI
        self.compare_crd_files_lbl = Label(master, text='\nCOMPARE CRD FILES\n')
        self.crd_file_1_btn = Button(master, text='(1) Choose CRD File 1: ', command=lambda: self.get_crd_file_path(1))
        self.crd_file_2_btn = Button(master, text='(2) Choose CRD File 2: ', command=lambda: self.get_crd_file_path(2))

        self.compare_crd_btn = Button(master, text='(3) COMPARE FILES ', command=self.compare_crd_files_outliers)
        self.compare_result_lbl = Label(master, text=' ')

        self.compare_crd_files_lbl.pack()
        self.crd_file_1_btn.pack()
        self.crd_file_2_btn.pack()
        self.compare_crd_btn.pack()
        self.compare_result_lbl.pack()

    def update_fixed_file(self):

        try:

            # open up fixed file & update the fixed file's easting/northings from the coordinate file
            fixed_file = FixedFile(self.fixed_file_path)
            coordinate_file = CoordinateFile(self.coordinate_file_path)
            fixed_file.update(coordinate_file)

        except Exception as ex:
            print(ex, type(ex))
            self.fixed_result_lbl.config(text='ERROR - See Richard')
            tkMessageBox.showerror("Error", ex)

        else:
            print("SUCCESS")
            self.fixed_result_lbl.config(text='SUCCESS')

    def compare_crd_files_outliers(self):

        # Tolerances - let user decide in GUI???

        tol_E = 0.005
        tol_N = 0.005

        common_points = []

        try:

            # open up the two CRD files and compare common values for outliers
            coordinate_file1 = CoordinateFile(self.crd_file_path_1)
            coordinate_file2 = CoordinateFile(self.crd_file_path_2)

            # find common points between files
            for key in coordinate_file1.coordinate_dictionary.keys():
                if key in coordinate_file2.coordinate_dictionary:
                    common_points.append(key)

            # Lets check for outliers for common points
            for point in common_points:
                cf1_E = float(coordinate_file1.coordinate_dictionary[point]['Eastings'])
                cf1_N = float(coordinate_file1.coordinate_dictionary[point]['Northings'])
                cf2_E = float(coordinate_file2.coordinate_dictionary[point]['Eastings'])
                cf2_N = float(coordinate_file2.coordinate_dictionary[point]['Northings'])

                diff_E = cf1_E - cf2_E
                diff_N = cf1_N - cf2_N

                if abs(diff_E) > tol_E:
                    self.outliers_dict[point] = "  Easting: " + '{0:.3f}'.format(round(diff_E, 3))
                if abs(diff_N) > tol_N:
                    self.outliers_dict[point] = "  Northing: " + '{0:.3f}'.format(round(diff_N, 3))

        except Exception as ex:
            print(ex, type(ex))
            self.compare_result_lbl.config(text='ERROR - See Richard\n')
            tkMessageBox.showerror("Error", ex)

        else:
            print("SUCCESS")
            self.compare_result_lbl.config(text='SUCCESS')

            # display results to user
            msg_header = "EASTING TOLERANCE = " + str(tol_E) + "\nNORTHING TOLERANCE = " + str(tol_N) +"\n\n"

            msg_body = ''

            for point in sorted(self.outliers_dict, key=lambda k: k):
                msg_body += point + ': ' + self.outliers_dict[point] + '\n'

            msg_complete = msg_header + msg_body

            top = Toplevel()
            top.title("POINTS THAT EXCEED TOLERANCE")
            top.geometry('400x600')

            msg = Message(top, text=msg_header + msg_body)
            msg.pack()

    def get_fixed_file_path(self):
        self.fixed_file_path = tkFileDialog.askopenfilename()
        print(self.fixed_file_path)

    def get_coordinate_file_path(self):
        self.coordinate_file_path = tkFileDialog.askopenfilename()
        print(self.coordinate_file_path)

    def get_crd_file_path(self, file_path_number):

        if file_path_number is 1:
            self.crd_file_path_1 = tkFileDialog.askopenfilename()
            print(self.crd_file_path_1)
        elif file_path_number is 2:
            self.crd_file_path_2 = tkFileDialog.askopenfilename()
            print(self.crd_file_path_2)
        else:

            tkMessageBox.showerror("Error", "No filepath no exists: " + str(file_path_number))


def main():
    # Create GUI - see GSI Query
    root = Tk()
    root.geometry("400x400")
    root.title(' THE GIGOLO by Richard Walter 2020')
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
