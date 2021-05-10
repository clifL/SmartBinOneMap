import random
import csv


def write_csv():
    fileName = 'WeightCalibration.csv'
    '''
    with open(fileName, mode='w', newline='') as calibration_file:
        calibration_writer = csv.writer(calibration_file,  quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writeData = []
        wr = csv.writer(calibration_file, quoting=csv.QUOTE_ALL)
        for i in range(100):
            writeData.append(random.randint(0,100))
        print(writeData)
        wr.writerow(writeData)
    '''
    with open(fileName, mode='w', newline='') as calibration_file:
        writeData = []
        calibration_writer = csv.writer(calibration_file,  quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for i in range(100):
            writeData.append(random.randint(0,100))
        calibration_writer.writerow(writeData)


write_csv()