import numpy as np
import pydicom
import os
import sys

class ScanLoader():
    def __init__(self, inputPath, **kwargs):
        self.__inputPath = inputPath
        try:
            '''
            Loading all patient information into a list
            Multiple patient information is expected to be stored in different
            patient folders in the inputPath
            '''
            self.__patientList = os.listdir(self.__inputPath)
            self.__patientList.sort()
        except IOError as e:
            print("I/O error({0}: {1} | Did you load from child directory directly?".format(e.errno, e.strerror))
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    def getPatientInfo(self):
        '''
        Method to show patient information on the console
        '''
        print("Total number of scans: ",str(len(self.__patientList)))
        idx = 0
        for i in self.__patientList:
            print('Index: ', idx, ' Scan_name: ', i)
            idx += 1

    def getPatientList(self):
        return self.__patientList
    
    def load_scan(self, path):
        print("Loading scan data")
        try:
            slices = [pydicom.read_file(path + '/' +s) for s in os.listdir(path)]
            slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
            try:
                slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
            except:
                slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

            for s in slices:
                s.SliceThickness = slice_thickness

            return slices
        except IOError as e:
            print("I/O error({0}: {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    def build_Hounsfield(self, slices):
        '''
        Method to take individual scan and convert to Hounsfield Units
        '''
        print("Building Hounsfield Unit data")
        image = np.stack([s.pixel_array for s in slices])
        image = image.astype(np.int16)

        image[image == -2000] = 0

        for slice_number in range(len(slices)):
            c = slices[slice_number].RescaleIntercept
            m = slices[slice_number].RescaleSlope
            if m != 1:
                image[slice_number] = m * image[slice_number].astype(np.float64)
                image[slice_number] = image[slice_number].astype(np.int16)
            image[slice_number] += np.int16(c)
        return np.array(image, dtype=np.int16)