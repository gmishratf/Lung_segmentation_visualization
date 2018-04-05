from ScanLoader import ScanLoader
from Plot2d import Plot2d
from ProcessData import ProcessData
#from PlotStatic3d import PlotStatic3d
from Visualize import Visualize
import Visualize as viz
import vtk

IP = input("Enter path containing scans: ")
loader = ScanLoader(IP)
loader.getPatientInfo()
patient_idx = input("Enter patient index for loading: ")
plist = loader.getPatientList()
bz = loader.load_scan(IP + plist[int(patient_idx)])
bz_voxels = loader.build_Hounsfield(bz)

dic_path = IP + str(plist[int(patient_idx)])

plotter = Plot2d()
plotter.plotHistogramHU(bz_voxels)
plotter.plotSlice(bz_voxels, int(len(bz_voxels)/2))
plotter.plotStack(bz_voxels)

processor = ProcessData()
bz_resampled, spacing = processor.resample(bz_voxels, bz, new_spacing=[1,1,1])
print("Original shape: ", bz_voxels.shape)
print("Resampled shape: ", bz_resampled.shape)
masked_lungs = processor.segment_lung(bz_resampled, False)
masked_lungs_filled = processor.segment_lung(bz_resampled, True)
#plotter3d = PlotStatic3d()
#plotter3d.plotStatic(bz_resampled)

viz.vis(dic_path, masked_lungs, masked_lungs_filled)