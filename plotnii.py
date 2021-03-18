import nibabel as nib
import pandas as pd
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from marching_cubes import march
#from marching_cubes.cpython37m import march
from numpy import load

import sys
   # Change the path to your path
  #print(max(volume))
def polygonize(volume):
  binvolume=volume>0.00001
# extract the mesh where the values are larger than or equal to 1
# everything else is ignored
  vertices, normals, faces = march(binvolume, 4)  # zero smoothing rounds
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
      print(v)
      f.write("v %.4f %.4f %.4f\n" % (v[0],v[1],v[2]))
    for face in faces:
      print(face)
      f.write("f %d %d %d\n" % (face[0]+1,face[1]+1,face[2]+1))
    for n in normals:
      print(n)
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
  blurred = gaussian_filter(nii_data, sigma=0.5)
  Main(blurred)

