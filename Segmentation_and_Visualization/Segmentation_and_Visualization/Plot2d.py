import matplotlib.pyplot as plt
class Plot2d():
    """description of class"""
    def plotHistogramHU(self, scan_voxels, bins=80, color='c'):
        '''
        Method to show histogram plot of hounsfield unit distribution in scan
        '''
        print("Plotting HU histogram")
        try:
            plt.hist(scan_voxels.flatten(), bins=bins, color=color)
            plt.xlabel("Hounsfield Units")
            plt.ylabel("Frequency")
            plt.show()
        except:
            print("Unexpected Error. Are you sure scan_voxels is in Hounsfield Units?")
            raise

    def plotSlice(self, scan_voxels, slice_number):
        '''
        Method to inspect individual slices in the scan data
        '''
        print("Plotting slice number {}".format(str(slice_number)))
        try:
            plt.imshow(scan_voxels[slice_number], cmap=plt.cm.gray)
            if(slice_number == (int(len(scan_voxels)/2))):
               plt.title('Middle slice')
            plt.show()
        except:
            print("Unexpected Error")
            raise

    def plotStack(self, scan, rows=6, cols=6, start_with=6, show_every=2):
        '''
        Method to inspect stack of slices in scan data
        '''
        print("Plotting stack of images")
        fig, ax = plt.subplots(rows, cols, figsize=[12, 12])
        for i in range(rows*cols):
            idx = start_with + i * show_every
            ax[int(i/rows), int(i%rows)].set_title('slice %d' % idx)
            ax[int(i/rows), int(i%rows)].imshow(scan[idx], cmap='gray')
            ax[int(i/rows), int(i%rows)].axis('off')
        plt.show()
