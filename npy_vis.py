import vtk
from vtk.util import numpy_support
import numpy as np

np_lung = np.load("./Vis_out/Masked_lungs.npy")
np_fill = np.load("./Vis_out/Masked_filled_lungs.npy")

np_trachea = np_fill - np_lung

vtk_lung = numpy_support.numpy_to_vtk(num_array=np_lung.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
vtk_trachea = numpy.support.numpy_to_vtk(num_array=np_trachea.ravel(), deep=True, array_type=vtk.VTK_FLOAT)

x, y, z = np_lung.shape
print(x, y, z)

dataImporter = vtk.vtkImageImport()
data_string = np_lung.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
dataImporter.SetDataScalarTypeToUnsignedChar()
dataImporter.SetNumberOfScalarComponents(1)
dataImporter.SetDataExtent(0, z-1, 0, y-1, 0, x-1)
dataImporter.SetWholeExtent(0, z-1, 0, y-1, 0, x-1)

# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
'''colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.55, 0.25, 0.15)
colorFunc.AddRGBPoint(94, 0.88, 0.60, 0.29)
colorFunc.AddRGBPoint(179, 1.0, 0.94, 0.95)
colorFunc.AddRGBPoint(260, 0.62, 0.0, 0.0)
colorFunc.AddRGBPoint(3071, 0.82, 0.66, 1.0)'''
colorFunc.AddRGBPoint(0, 85 / 255.0, 0.0, 0.0)
#colorFunc.AddRGBPoint(95, 1.0, 1.0, 1.0)
#colorFunc.AddRGBPoint(225, 0.66, 0.66, 0.5)
#colorFunc.AddRGBPoint(255, 0.3, 1.0, 0.5)
#colorFunc.AddRGBPoint(0, 0.0, 0.0, 0.0)
#colorFunc.AddRGBPoint(255, 0.3, 0.3, 0.9)


# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
'''alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
#alphaChannelFunc.AddPoint(0, 0.2)
alphaChannelFunc.AddPoint(94, 0.01)
alphaChannelFunc.AddPoint(179, 0.01)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)'''
alphaChannelFunc.AddPoint(0, 0.0)
alphaChannelFunc.AddPoint(255, 1.0)
alphaChannelFunc.AddPoint(3, 10.0)


# Creating volume
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorFunc)
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# Creating mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(800,800)

volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty) 

# Add the volume to the renderer
ren.AddVolume(volume)
#ren.AddActor(imageActor)

light = vtk.vtkLight()
light.SetColor(1.0, 1.0, 1.0)
ren.AddLight(light)
ren.SetBackground(1.0, 1.0, 1.0)

# Render the scene
renWin.Render()
iren.Start()

'''
img_vtk = vtk.vtkImageData()
img_vtk.SetDimensions(np_lung.shape)
#img_vtk.SetSpacing(spacing[::-1])
img_vtk.GetPointData().SetScalars(vtk_lung)

volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(800,800)
'''

'''
cmap = vtk.vtkImageMapToWindowLevelColors()
cmap.SetOutputFormatToLuminance()
cmap.SetInputData(reader.GetOutput())
cmap.SetWindow(1000.0)
cmap.SetWindow(400.0)
cmap.UpdateWholeExtent()

imageActor = vtk.vtkImageActor()
imageActor.SetInputData(cmap.GetOutput())

'''




'''
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(r"F:\python stuff\bzCT_Vis_scikit\GSM714044\1.3.6.1.4.1.14519.5.2.1.4334.1501.305837811806532074576487712656\1.3.6.1.4.1.14519.5.2.1.4334.1501.141336442320900896496732659416")
reader.Update()

# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
#colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.54902, 0.25098, 0.14902)
colorFunc.AddRGBPoint(94, 0.882353, 0.603922, 0.290196)
colorFunc.AddRGBPoint(179, 1, 0.937033, 0.954531)
#colorFunc.AddRGBPoint(260, 0.615686, 0, 0)
#colorFunc.AddRGBPoint(3071, 0.827451, 0.658824, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(94, 0.29)
alphaChannelFunc.AddPoint(179, 0.55)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)

# Instantiate necessary classes and create VTK pipeline
volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(800,800)

# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)  

# Add the volume to the renderer
ren.AddVolume(volume)

# Render the scene
renWin.Render()
iren.Start()
'''