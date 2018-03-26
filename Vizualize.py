import vtk
from vtk.util import numpy_support
import numpy as np

class Visualize:
	def __init__(self):
		self.__ren = vtk.vtkRenderer()
		self.__colorFunc = vtk.vtkColorTransferFunction()
		self.__alphaChannelFunc = vtk.vtkPiecewiseFunction()
		
	def viz_SetViewport(self, xmin, xmax, ymin, ymax):
		self.__ren.SetViewport(xmin, xmax, ymin, ymax)
		
	def viz_AddColorFunctionPoint(self, p, r, g, b):
		self.__colorFunc.AddRGBPoint(p, r, g, b)
		
	def viz_AddOpacityFunctionPoint(self, p, val):
		self.__alphaChannelFunc.AddPoint(p, val)
		
	def viz_SetDataUsingPath(self, path):
		data = np.load(path)
		self.viz_SetData(data)
		
	def viz_SetData(self, data):
		self.__dataImporter = vtk.vtkImageImport()
		data_string = data.tostring()
		x, y, z = data.shape
		self.__dataImporter.CopyImportVoidPointer(data_string, len(data_string))
		self.__dataImporter.SetDataScalarTypeToUnsignedChar()
		self.__dataImporter.SetNumberOfScalarComponents(1)
		self.__dataImporter.SetDataExtent(0, z-1, 0, y-1, 0, x-1)
		self.__dataImporter.SetWholeExtent(0, z-1, 0, y-1, 0, x-1)
		
	def viz_SetLighting(self, r, g, b):
		light = vtk.vtkLight()
		light.SetColor(r, g, b)
		self.__ren.AddLight(light)
		
	def viz_SetBackground(self, r, g, b):
		self.__ren.SetBackground(r, g, b)
		
	def viz_visualize(self):
		volume = vtk.vtkVolume()
		volumeProperty = vtk.vtkVolumeProperty()
		volumeProperty.SetColor(self.__colorFunc)
		volumeProperty.SetScalarOpacity(self.__alphaChannelFunc)
		volumeProperty.ShadeOn()
		volumeProperty.SetInterpolationTypeToLinear()
		volumeMapper = vtk.vtkSmartVolumeMapper()
		volumeMapper.SetInputConnection(self.__dataImporter.GetOutputPort())
		volume.SetMapper(volumeMapper)
		volume.SetProperty(volumeProperty) 
		self.__ren.AddVolume(volume)
	
	def GetRenderer(self):
		return self.__ren

def main():
	# Renderers
	viz1, viz2, viz3, viz4, viz5, viz6, viz7 = [Visualize() for i in range(7)]
	
	# Setting viewports for renderers
	viz1.viz_SetViewport(0.0, 0.5, 0.333333, 1.0)
	viz2.viz_SetViewport(0.333333, 0.5, 0.666666, 1.0)
	viz3.viz_SetViewport(0.666666, 0.5, 1.0, 1.0)
	viz4.viz_SetViewport(0.0, 0.0, 0.25, 0.5)
	viz5.viz_SetViewport(0.25, 0.0, 0.5, 0.5)
	viz6.viz_SetViewport(0.5, 0.0, 0.75, 0.5)
	viz7.viz_SetViewport(0.75, 0.0, 1.0, 0.5)
	
	# Setting background
	viz1.viz_SetBackground(1.0, 1.0, 1.0)
	viz2.viz_SetBackground(1.0, 1.0, 1.0)
	viz3.viz_SetBackground(1.0, 1.0, 1.0)
	viz4.viz_SetBackground(1.0, 1.0, 1.0)
	viz5.viz_SetBackground(1.0, 1.0, 1.0)
	viz6.viz_SetBackground(1.0, 1.0, 1.0)
	viz7.viz_SetBackground(1.0, 1.0, 1.0)
	
	# Reading Data
	np_lung = np.load("./Vis_out/Masked_lungs.npy")
	np_fill = np.load("./Vis_out/Masked_filled_lungs.npy")
	np_trachea = np_fill - np_lung
	
	# Setting Data
	viz1.viz_SetData(np_fill)
	viz2.viz_SetData(np_lung)
	viz3.viz_SetData(np_trachea)
	
	# Adding color
	viz1.viz_AddColorFunctionPoint(0, 0.0, 0.0, 0.0)
	viz2.viz_AddColorFunctionPoint(0, 0.0, 0.0, 0.0)
	viz3.viz_AddColorFunctionPoint(0, 0.0, 0.0, 0.0)
	viz1.viz_AddColorFunctionPoint(255, 0.3, 0.3, 0.9)
	viz2.viz_AddColorFunctionPoint(255, 0.3, 0.3, 0.9)
	viz3.viz_AddColorFunctionPoint(255, 0.3, 0.3, 0.9)
	
	# Adding Opacity
	viz1.viz_AddOpacityFunctionPoint(0, 0.0)
	viz1.viz_AddOpacityFunctionPoint(255, 1.0)
	viz1.viz_AddOpacityFunctionPoint(3, 10.0)
	
	viz2.viz_AddOpacityFunctionPoint(0, 0.0)
	viz2.viz_AddOpacityFunctionPoint(255, 1.0)
	viz2.viz_AddOpacityFunctionPoint(3, 10.0)
	
	viz3.viz_AddOpacityFunctionPoint(0, 0.0)
	viz3.viz_AddOpacityFunctionPoint(255, 1.0)
	viz3.viz_AddOpacityFunctionPoint(3, 10.0)
	
	# Setting light
	viz1.viz_SetLighting(1.0, 1.0, 1.0)
	viz2.viz_SetLighting(1.0, 1.0, 1.0)
	viz3.viz_SetLighting(1.0, 1.0, 1.0)
	
	# Final steps for visualizing
	viz1.viz_visualize()
	viz2.viz_visualize()
	viz3.viz_visualize()
	
	# Renderer window
	renWin = vtk.vtkRenderWindow()
	renWin.AddRenderer(viz1.GetRenderer())
	renWin.AddRenderer(viz2.GetRenderer())
	renWin.AddRenderer(viz3.GetRenderer())
	renWin.AddRenderer(viz4.GetRenderer())
	renWin.AddRenderer(viz5.GetRenderer())
	renWin.AddRenderer(viz6.GetRenderer())
	renWin.AddRenderer(viz7.GetRenderer())
	
	iren = vtk.vtkRenderWindowInteractor()
	iren.SetRenderWindow(renWin)
	renWin.SetFullScreen(1)
	renWin.Render()
	iren.Start()
	

main()


'''
ren1.SetBackground(0.0, 0.0, 0.0)
	ren2.SetBackground(1.0, 0.0, 0.0)
	ren3.SetBackground(0.0, 1.0, 0.0)
	ren4.SetBackground(0.0, 0.0, 1.0)
	ren5.SetBackground(1.0, 1.0, 0.0)
	ren6.SetBackground(0.0, 1.0, 1.0)
	ren7.SetBackground(1.0, 0.0, 1.0) 
	
	viz1.viz_SetBackground(0.0, 0.0, 0.0)
	viz2.viz_SetBackground(1.0, 0.0, 0.0)
	viz3.viz_SetBackground(0.0, 1.0, 0.0)
	viz4.viz_SetBackground(0.0, 0.0, 1.0)
	viz5.viz_SetBackground(1.0, 1.0, 0.0)
	viz6.viz_SetBackground(0.0, 1.0, 1.0)
	viz7.viz_SetBackground(1.0, 0.0, 1.0)'''



