from ctypes import *
import random
import csv

#so_file = "/Users/lamzh/Desktop/SterilizeData.so"
#my_functions = CDLL(so_file)


with open('WeightCalibration.csv', mode='w', newline='') as calibration_file:
    calibration_writer = csv.writer(calibration_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    calibration_writer.writerow(['John Smith', 'Accounting', 'November'])
    calibration_writer.writerow(['Erica Meyers', 'IT', 'March'])
    calibration_writer.writerow(['FF Meyers', 'IT', 'March'])


with open('WeightCalibration.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')

print("Done")