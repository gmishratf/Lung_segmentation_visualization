# Lung_segmentation_visualization
Segment DICOM chest scan to retrieve lung and trachea. Visualization using VTK.  
Open visual studio solution ./Segmentation_and_visualization/Segmentation_and_visualization.sln  
  
Set test_main.py as startup file.  
  
Dependencies:  
- pydicom v1 or above   
- VTK v7 and above  
- Python 3  
- numpy  
- scipy  
- scikit-image  
- matplotlib  
- plotly  

TODO:  
1. Set vtkimageplanes for lung slicing
2. Fix static plotting class (Matplotlib and plotly unable to handle million+ data points)

FIXED:
1. Fixed viewport 1  
2. Fixed datasets, uploaded better sample datasets.  
3. Fixed camera for touch screen inputs.  
4. Fixed dataset labels.  
