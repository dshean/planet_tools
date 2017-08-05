#! /bin/bash

#Skeleton framework to orthorectify Planet MS image products 
#Input Level 1B image 
#For MS products, band order is BGRN. For 3-band products, RGB.

set -e

#img=~/Documents/UW/Planet/planet_order_52815/20170411_181913_0e0f/20170411_181913_0e0f_1B_AnalyticMS.tif
img=$1

#This is the DEM to use for orthorectification
dem=$2
#dem=/Volumes/SHEAN_1TB_SSD/site_poly_highcount_rect3_rerun/rainier/mos_seasonal_summer-tile-0.tif

if [ "$#" -ne 2 ] ; then
    echo "Usage is \`$(basename $0) img_1B_AnalyticMS.tif dem.tif\`"
    exit
fi

#Delete intermediate products
cleanup=true

#Automatically determine projection
#Requires proj_select.py utility in pygeotools
#Note, L1B metadata does not have corner coordinates specified
#proj="$(proj_select.py $img)"
lat=$(gdalinfo $img | grep LAT_OFF | awk -F'=' '{print $NF}')
lon=$(gdalinfo $img | grep LONG_OFF | awk -F'=' '{print $NF}')
proj="$(proj_select.py $lat $lon)"
#proj="EPSG:32610"

#Can specify extent here
#extent_proj2px.py can be used to limit the gdal_translate step
#or --t_projwin for mapproject step

#Extract bands to separate files
blist="1 2 3 4"
echo "Extracting bands: $blist"
parallel --verbose "if [ ! -e ${img%.*}_b{}.tif ] ; then gdal_translate -b {} -co TILED=YES -co COMPRESS=LZW -co BIGTIFF=IF_SAFER $img ${img%.*}_b{}.tif ; fi" ::: $blist

#Orthorecrify each band separately
#Note: ASP mapproject is multithreaded and will efficiently use all CPUs
echo "Orthorectifying using: $dem"
for b in $blist
do
    if [ ! -e ${img%.*}_b${b}_ortho.tif ] ; then
        mapproject -t rpc --t_srs "$proj" $dem ${img%.*}_b${b}.tif ${img%.*}_b${b}_ortho.tif
    fi
done

#Now recombine into RGB image
n=${img%.*}_b4_ortho.tif
r=${img%.*}_b3_ortho.tif
g=${img%.*}_b2_ortho.tif
b=${img%.*}_b1_ortho.tif

#Create composites
echo "Creating RGB composite"
gdalbuildvrt -separate ${img%.*}_ortho_RGB.vrt $r $g $b
echo "Creating NRG composite"
gdalbuildvrt -separate ${img%.*}_ortho_NRG.vrt $n $r $g
echo "Calculating NDVI"
gdal_calc.py --overwrite --calc "(A-B)/(A+B)" -A $n -B $r --NoDataValue 0.0 --outfile ${img%.*}_ortho_NDVI.tif 

if $cleanup ; then
    for b in $blist
    do
        rm ${img%.*}_b${b}.tif
    done
fi
