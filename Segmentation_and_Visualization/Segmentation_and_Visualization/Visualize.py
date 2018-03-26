import vtk
from vtk.util import numpy_support
import numpy as np

class Visualize():
    def __init__(self):
        self.__ren = vtk.vtkRenderer()
        self.__colorFunc = vtk.vtkColorTransferFunction()
        self.__alphaChannelFunc = vtk.vtkPiecewiseFunction()

    def viz_SetViewport(self, xmin, xmax, ymin, ymax):
        self.__ren.SetViewport(xmin, xmax, ymin, ymax)

    def viz_SetViewportName(self, name, x, y, fontsize=14, color=[0,0,0]):
        text = vtk.vtkTextActor()
        text.SetInput(name)
        text.SetPosition(x, y)
        text.GetTextProperty().SetFontSize(fontsize)
        text.GetTextProperty().SetColor(color[0], color[1], color[2])
        self.__ren.AddActor2D(text)

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
        self.__dataImporter.SetDataExtent(0, z - 1, 0, y - 1, 0, x - 1)
        self.__dataImporter.SetWholeExtent(0, z - 1, 0, y - 1, 0, x - 1)

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
        volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
        volumeMapper.SetInputConnection(self.__dataImporter.GetOutputPort())
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty) 
        self.__ren.AddVolume(volume)

    def GetRenderer(self):
        return self.__ren

def vis(scan, np_lung, np_fill):
    # Renderers
    viz1, viz2, viz3, viz4, viz5, viz6, viz7 = [Visualize() for i in range(7)]

    # Setting Viewports
    viz1.viz_SetViewport(0.0, 0.502, 0.331, 1.0)
    viz2.viz_SetViewport(0.335, 0.502, 0.664, 1.0)
    viz3.viz_SetViewport(0.668, 0.502, 1.0, 1.0)
    viz4.viz_SetViewport(0.0, 0.0, 0.248, 0.498)
    viz5.viz_SetViewport(0.252, 0.0, 0.498, 0.498)
    viz6.viz_SetViewport(0.502, 0.0, 0.748, 0.498)
    viz7.viz_SetViewport(0.752, 0.0, 1.0, 0.498)

    viz1.viz_SetViewportName('Original Scan', 10, 25)
    viz2.viz_SetViewportName('Segmented Lungs', 10, 25)
    viz3.viz_SetViewportName('Segmented Trachea', 10, 25)
    viz4.viz_SetViewportName('Right lung', 10, 25)
    viz5.viz_SetViewportName('Right trachea', 10, 25)
    viz6.viz_SetViewportName('Left lung', 10, 25)
    viz7.viz_SetViewportName('Left trachea', 10, 25)

    # Setting background
    viz1.viz_SetBackground(1.0, 1.0, 1.0)
    viz2.viz_SetBackground(1.0, 1.0, 1.0)
    viz3.viz_SetBackground(1.0, 1.0, 1.0)
    viz4.viz_SetBackground(1.0, 1.0, 1.0)
    viz5.viz_SetBackground(1.0, 1.0, 1.0)
    viz6.viz_SetBackground(1.0, 1.0, 1.0)
    viz7.viz_SetBackground(1.0, 1.0, 1.0)

    # Getting data
    np_trachea = np_fill - np_lung
    # m_r = np_lung[:, :int(np_lung.shape[1] / 2), :int(np_lung.shape[2] / 2)]
    # m_l = np_lung[:, int(np_lung.shape[1] / 2):, int(np_lung.shape[2] / 2):]
    m_r = np_lung[:, :, :int(np_lung.shape[2] / 2)]
    m_l = np_lung[:, :, int(np_lung.shape[2] / 2):]
    
    # m_f_r = np_fill[:, :int(np_fill.shape[1] / 2), :int(np_fill.shape[2] / 2)]
    # m_f_l = np_fill[:, int(np_fill.shape[1] / 2):, int(np_fill.shape[2] / 2):]
    m_f_r = np_fill[:, :, :int(np_fill.shape[2] / 2)]
    m_f_l = np_fill[:, :, int(np_fill.shape[2] / 2):]
    
    # m_pul_r = np_trachea[:, :int(np_trachea.shape[1] / 2), :int(np_trachea.shape[2] / 2)]
    # m_pul_l = np_trachea[:, int(np_trachea.shape[1] / 2):, int(np_trachea.shape[2] / 2):]
    m_pul_r = np_trachea[:, :, :int(np_trachea.shape[2] / 2)]
    m_pul_l = np_trachea[:, :, int(np_trachea.shape[2] / 2):]
    try:
        r_ratio = np.count_nonzero(m_pul_r) / np.count_nonzero(m_r)
    except:
        r_ratio = 0.0
    try:
        l_ratio = np.count_nonzero(m_pul_l) / np.count_nonzero(m_l)
    except:
        l_ratio = 0.0
    
    r_vol = np.count_nonzero(m_r)/1000
    l_vol = np.count_nonzero(m_l)/1000

    
    viz4.viz_SetViewportName("R Lung volume: {:.5f} cc".format(r_vol), 10, 50)
    viz5.viz_SetViewportName("R Trachea to lung volume ratio: {:.5f}".format(r_ratio), 10, 50)
    viz6.viz_SetViewportName("L Lung volume: {:.5f} cc".format(l_vol), 10, 50)
    viz7.viz_SetViewportName("L Trachea to lung volume ratio: {:.5f}".format(l_ratio), 10, 50)

    # Setting Data
    viz1.viz_SetData(scan)
    viz2.viz_SetData(np_lung)
    viz3.viz_SetData(np_trachea)
    viz4.viz_SetData(m_r)
    viz5.viz_SetData(m_pul_r)
    viz6.viz_SetData(m_l)
    viz7.viz_SetData(m_pul_l)
    
    # Adding color
    viz1.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)
    viz2.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)
    viz3.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)
    viz4.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)
    viz5.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)
    viz6.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)
    viz7.viz_AddColorFunctionPoint(0, 85/255.0, 0.0, 0.0)

    # Adding Opacity
    viz1.viz_AddOpacityFunctionPoint(0, 0.0)
    viz1.viz_AddOpacityFunctionPoint(255, 1.0)
    viz1.viz_AddOpacityFunctionPoint(3, 10.0)

    viz2.viz_AddOpacityFunctionPoint(0, 0.0)
    viz2.viz_AddOpacityFunctionPoint(255, 1.0)
    viz2.viz_AddOpacityFunctionPoint(3, 0.2)

    viz3.viz_AddOpacityFunctionPoint(0, 0.0)
    viz3.viz_AddOpacityFunctionPoint(255, 1.0)
    viz3.viz_AddOpacityFunctionPoint(3, 10.0)

    viz4.viz_AddOpacityFunctionPoint(0, 0.0)
    viz4.viz_AddOpacityFunctionPoint(255, 1.0)
    viz4.viz_AddOpacityFunctionPoint(3, 0.2)

    viz5.viz_AddOpacityFunctionPoint(0, 0.0)
    viz5.viz_AddOpacityFunctionPoint(255, 1.0)
    viz5.viz_AddOpacityFunctionPoint(3, 10.0)

    viz6.viz_AddOpacityFunctionPoint(0, 0.0)
    viz6.viz_AddOpacityFunctionPoint(255, 1.0)
    viz6.viz_AddOpacityFunctionPoint(3, 0.2)

    viz7.viz_AddOpacityFunctionPoint(0, 0.0)
    viz7.viz_AddOpacityFunctionPoint(255, 1.0)
    viz7.viz_AddOpacityFunctionPoint(3, 10.0)

    # Setting light
    viz1.viz_SetLighting(1.0, 1.0, 1.0)
    viz2.viz_SetLighting(5.0, 5.0, 5.0)
    viz3.viz_SetLighting(1.0, 1.0, 1.0)
    viz4.viz_SetLighting(10.0, 10.0, 10.0)
    viz5.viz_SetLighting(1.0, 1.0, 1.0)
    viz6.viz_SetLighting(10.0, 10.0, 10.0)
    viz7.viz_SetLighting(1.0, 1.0, 1.0)

    # Final steps for visualizing
    viz1.viz_visualize()
    viz2.viz_visualize()
    viz3.viz_visualize()
    viz4.viz_visualize()
    viz5.viz_visualize()
    viz6.viz_visualize()
    viz7.viz_visualize()

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