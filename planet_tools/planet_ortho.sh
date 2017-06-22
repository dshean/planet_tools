#! /bin/bash

#For any multispectral asset, the order is BGRN. For any 3 band asset, it is RGB.

dir=~/Documents/UW/Planet/planet_order_52815/20170411_181913_0e0f
img=20170411_181913_0e0f_1B_AnalyticMS.tif
dem=/Volumes/SHEAN_1TB_SSD/site_poly_highcount_rect3_rerun/rainier/mos_seasonal_summer-tile-0.tif
epsg=32610
parallel "gdal_translate -b {} -co TILED=YES -co COMPRESS=LZW -co BIGTIFF=IF_SAFER $img ${img%.*}_b{}.tif" ::: 1 2 3 4
for b in 1 2 3 4
do
    mapproject --t_srs EPSG:$epsg $dem ${img%.*}_b${b}.tif ${img%.*}_b${b}_ortho.tif
done
gdalbuildvrt -separate ${img%.*}_ortho.vrt ${img%.*}_b3_ortho.tif ${img%.*}_b2_ortho.tif ${img%.*}_b1_ortho.tif
