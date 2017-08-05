#! /usr/bin/env python

"""
Utility to open and display all bands from Planet udm and 1B images.
"""

import sys

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

from pygeotools.lib import iolib,malib
from imview.lib import pltlib

udm_b_txt = ['Blackfill', 'Cloud', 'Blue missing', 'Green missing', 'Red missing', \
        'RedEdge missing', 'NIR missing', 'Unused'] 
img_b_txt = ['B','G','R','NIR']

fn = sys.argv[1]

if 'udm' in fn:
    #fn = '20170411_181913_0e0f_1B_AnalyticMS_DN_udm.tif'
    udm = iolib.fn_getma(fn)
    #udm_b = np.unpackbits(udm.ravel(), axis=0).reshape(udm.shape+(8,))
    udm_b = np.unpackbits(udm.ravel()[:,np.newaxis], axis=1).reshape(udm.shape+(8,))
    f,axa = plt.subplots(8, sharex=True, sharey=True, figsize=(4,8))
    for i in range(udm_b.shape[2]):
        axa[i].imshow(udm_b[:,:,i], clim=(0,1), cmap='gray')
        axa[i].set_title(udm_b_txt[i])
        #pltlib.hide_ticks(axa[i])
        axa[i].axis('off')
else:
    #fn = '20170411_181913_0e0f_3B_AnalyticMS.tif'
    img_ds = gdal.Open(fn)
    img = np.ma.array([iolib.ds_getma(img_ds, i+1) for i in range(img_ds.RasterCount)])
    f,axa = plt.subplots(4, sharex=True, sharey=True, figsize=(4,4))
    for i in range(img.shape[0]):
        axa[i].imshow(img[i], clim=(1,25000), cmap='gray')
        axa[i].set_title(img_b_txt[i])
        #pltlib.hide_ticks(axa[i])
        axa[i].axis('off')

plt.tight_layout()
plt.show()
