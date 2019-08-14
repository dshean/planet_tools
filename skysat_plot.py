#! /usb/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#eci2ecef

#conv
def conv(az1, el1, az2, el2):
    from numpy import deg2rad as d2r
    from numpy import rad2deg as r2d
    conv_ang = r2d(np.arccos(np.sin(d2r(el1))*np.sin(d2r(el2)) + np.cos(d2r(el1))*np.cos(d2r(el2))*np.cos(d2r(az1 - az2))))
    return conv_ang

#bh
#base = np.sqrt(alt1**2 + alt2**2 - 2*alt1*alt2*np.cos(d2r(conv_ang)))
#bh = base/np.mean([alt1, alt2])

csv_fn=sys.argv[1]
df = pd.read_csv(csv_fn)

fig1 = plt.figure()
ax = plt.subplot(111, polar=True)
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
ax.grid(True)

az = np.deg2rad(df['sat_az'])
el = 90 - df['sat_elev']
ax.scatter(az, el, color='r', s=3)
ax.set_rmin(0)
ax.set_rmax(70)

az1, el1 = df[['sat_az', 'sat_elev']].iloc[0]
az2, el2 = df[['sat_az', 'sat_elev']].iloc[-1]
max_conv = conv(az1, el1, az2, el2)
print("Max conv angle: %0.2f" % max_conv)

title = csv_fn
title += "\nMax. conv.: %0.2f" % max_conv
ax.set_title(title)
fig_fn = os.path.splitext(csv_fn)[0]+'.pdf'
plt.savefig(fig_fn)
