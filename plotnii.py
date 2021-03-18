import nibabel as nib
import pandas as pd
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from marching_cubes import march
#from marching_cubes.cpython37m import march
from numpy import load

import sys

def polygonize(volume):
  print(volume)
  print(volume.shape)
  d1,d2,d3=volume.shape
  values=volume.reshape(d1*d2*d3)
  print(max(values))
  print(min(values))
  binvolume=volume>0.1 #misael
#  binvolume=volume>100 #syntetic
# extract the mesh where the values are larger than or equal to 1
# everything else is ignored
  print("MC starting..!")
  vertices, normals, faces = march(binvolume, 0)  # zero smoothing rounds
#  smooth_vertices, smooth_normals, faces = march(volume, 4)  # 4 smoothing rounds
  print("MC done..!")
#  print(vertices,normals,faces)
  return vertices, normals, faces

def Main(blured):
  from pyqtgraph.opengl import GLViewWidget, MeshData
  from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem
  from PyQt5.QtGui import QApplication

  app = QApplication([])
  view = GLViewWidget()

  vertices, normals, faces= polygonize(blured)
  with open(sys.argv[2], 'w') as f:
    f.write("# OBJ file\n")
    for v in vertices:
      f.write("v %.4f %.4f %.4f\n" % (v[0],v[1],v[2]))
    for face in faces:
      f.write("f %d %d %d\n" % (face[0]+1,face[1]+1,face[2]+1))
    for n in normals:
      f.write("n %.4f %.4f %.4f\n" % (n[0],n[1],n[2]))

  mesh = MeshData(vertices/100 , faces)  # scale down - because camera is at a fixed position 
# or mesh = MeshData(smooth_vertices / 100, faces)
  mesh._vertexNormals = normals
# or mesh._vertexNormals = smooth_normals

  item = GLMeshItem(meshdata=mesh, color=[1, 0, 0, 1], shader="normalColor")

  view.addItem(item)
  view.show()
  app.exec_()

if __name__ == "__main__":
  if(len(sys.argv)<2):
    print("Wrong parameters ...!")
    print("python3 plotnii.py file")
    exit()
 #resolution 500, 250, etc
  path = sys.argv[1] #'path to img.nii.gz'
  Nifti_img  = nib.load(path)
  nii_data = Nifti_img.get_fdata()
  print(nii_data.shape)
  if len(nii_data.shape)>3:
    d1,d2,d3,d4=nii_data.shape
    nii_data=nii_data.reshape(d1,d2,d3)
  blurred = gaussian_filter(nii_data, sigma=0.5)
  blurred = gaussian_filter(blurred, sigma=0.5)
  Main(blurred)

