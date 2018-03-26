import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
import numpy as np
import plotly
from plotly import figure_factory
from plotly.graph_objs import *

class PlotStatic3d():
    """description of class"""
    def __init__(self, figsize=(10,10), alpha=0.70, face_color=[0.25, 0.5, 0.75], **kwargs):
        self.figsize = figsize
        self.alpha = alpha
        self.face_color = face_color

    def __build_mesh(self, image, threshold=300, step_size=1):
        '''
        Helper method to build mesh for given 3D scan
        '''
        print("Transposing surface")
        p = image.transpose(2, 1, 0)
        print("Generating mesh")
        verts, faces, _, _ = measure.marching_cubes(p, threshold,
                                                   step_size=step_size)#, 
                                                   #allow_degenerate=True)
        return verts, faces, p

    def plotStatic(self, image, threshold=300, step_size=1):
        '''
        Method to visualize a static plot of given 3D scan
        '''
        verts, faces, p = self.__build_mesh(image, threshold, step_size)
        print("Drawing")
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        mesh = Poly3DCollection(verts[faces], alpha=self.alpha)
        mesh.set_facecolor(self.face_color)
        ax.add_collection3d(mesh)
        ax.set_xlim(0, p.shape[0])
        ax.set_ylim(0, p.shape[1])
        ax.set_zlim(0, p.shape[2])
        print("Plotting")
        plt.show()

    def plotInteractive(self, image, threshold=300, step_size=1):
        '''
        Method to visualize interactive plot using plotly
        Might crash, try at own risk
        '''
        verts, faces, p = self.__build_mesh(image, threshold, step_size)
        print("Drawing")
        x, y, z = zip(*verts)
        colormap = ['rgb(236,236,212)', 'rgb(236,236,212)']
        fig = figure_factory.create_trisurf(x=x, 
                               y=y, 
                               z=z,
                               plot_edges = False,
                               colormap = colormap,
                               simplices = faces,
                               backgroundcolor = 'rgb(64, 64, 64)',
                               title = "Interactive Visualization")
        print('Plotting')
        plotly.plotly.plot(fig)