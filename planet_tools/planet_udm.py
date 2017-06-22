#! /usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
from pygeotools.lib import iolib,malib
from imview.lib import pltlib

udm_fn = '/Users/dshean/Documents/UW/Planet/planet_order_52815/20170411_181913_0e0f/20170411_181913_0e0f_1B_AnalyticMS_DN_udm.tif'
udm = iolib.fn_getma(udm_fn)
#udm_b = np.unpackbits(udm.ravel(), axis=0).reshape(udm.shape+(8,))
udm_b = np.unpackbits(udm.ravel()[:,np.newaxis], axis=1).reshape(udm.shape+(8,))
f,axa = plt.subplots(8, sharex=True, sharey=True, figsize=(4,8))
udm_b_txt = ['Blackfill', 'Cloud', 'Blue missing', 'Green missing', 'Red missing', 'RedEdge missing', 'NIR missing', 'Unused'] 
for i in range(udm_b.shape[2]):
    axa[i].imshow(udm_b[:,:,i], clim=(0,1), cmap='gray')
    axa[i].set_title(udm_b_txt[i])
    pltlib.hide_ticks(axa[i])
plt.tight_layout()
plt.show()
