import scipy.ndimage
from skimage import measure
import numpy as np
import pydicom

class ProcessData():
    """description of class"""
    #def __init__(self, **kwargs):
    #    return

    def resample(self, image, scan, new_spacing=[1,1,1]):
        '''
        Method to normalize voxel dimensions for easier processing during
        segmentation and visualization
        '''
        print("Resampling data for voxel normalization")
        if scan[0].SliceThickness == 0.0:
            scan[0].SliceThickness = 1.0
        current_spacing = []
        current_spacing.append(np.float32(scan[0].SliceThickness))
        current_spacing.append(np.float32(scan[0].PixelSpacing[0]))
        current_spacing.append(np.float32(scan[0].PixelSpacing[1]))
        current_spacing = np.array(current_spacing, dtype=np.float32)
        # calculate resize factor on basis of new_spacing
        resize_factor = current_spacing / new_spacing
        # finding new volume
        new_real_shape = image.shape * resize_factor
        # rounding values for better plotting
        new_shape = np.round(new_real_shape)
        # finding real resizing factor
        real_resize_factor = new_shape / image.shape
        # normalizing new spacing by real resizing factor
        new_spacing = current_spacing / real_resize_factor
        # interpolating image with real resizing factor
        image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
        return image, new_spacing

    # Segmentation by region growing and morphological operation
    # 4 steps:
    #    Threshold with -320 HU
    #    Connect components and determine label of air around patient, fill air with 1s in binary mask
    #    Find largest connected solid component for every axial slice in scan, and set others to 0 \
    #    Keep only largest air pocket
    def __largest_volume(self, image, background=-1):
        '''
        Helper function to calculate largest consecutive volume in lung scan
        '''
        values, counts = np.unique(image, return_counts=True)
        counts = counts[values != background]
        values = values[values != background]
        if len(counts) > 0:
            return values[np.argmax(counts)]
        else:
            return None

    def segment_lung(self, image, fill_lung=True):
        print("Segmenting lungs")
        masked_image = np.array(image > -320, dtype=np.int8)+1
        labels = measure.label(masked_image)
        # Pick absolute corner pixel to find label for air
        bg_label = labels[0,0,0]
        # Fill air around patient to 2
        masked_image[bg_label == labels] = 2
        # Fill the lung structure 
        if fill_lung:
            for i, axial_slice in enumerate(masked_image):
                axial_slice = axial_slice - 1
                labeling = measure.label(axial_slice)
                l_max = self.__largest_volume(labeling, background=0)
                if l_max is not None:
                    masked_image[i][labeling != l_max] = 1
        # Setting actual image to binary
        masked_image -= 1
        # Inverting to set lungs to 1
        masked_image = 1 - masked_image
        # Removing air pockets inside body
        labels = measure.label(masked_image, background=0)
        l_max = self.__largest_volume(labels, background=0)
        if l_max is not None:
            masked_image[labels != l_max] = 0
        return masked_image