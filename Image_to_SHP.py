### CREATES SHAPEFILES BASED ON GPS METADATA FOUND IN IMAGES PROVIDED BY USER

import os
import arcpy
from PIL import Image, ExifTags

folder = r'F:\Pictures\2016\iPhone Pics\rename_test'  # INPUT A FOLDER THAT HAS PICTURES IN IT
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)
arcpy.env.overwriteOutput = True
num = 0
num2 = 0
shp_list = []  # used to make one shapefile containing all points instead of shapefiles for all points


def image_to_shp():
    global num, x, root, long_in_degrees,lat_in_degrees, shp_list, num2

    for root, dir2, files in os.walk(folder):
        print 'Creating shapefiles from images in {} \n'.format(root)
        if len(dir2) > 0:
            print 'Found the following sub folders {} \n'.format(dir2)

        for x in files:
            if x.lower().endswith('.jpg'):
                img = Image.open(os.path.join(root, x))
                exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
                    }
                gps_all = {}

                try:
                    for key in exif['GPSInfo'].keys():
                        decode = ExifTags.GPSTAGS.get(key, key)
                        gps_all[decode] = exif['GPSInfo'][key]

                    long_ref = gps_all.get('GPSLongitudeRef')
                    lat_ref = gps_all.get('GPSLatitudeRef')

                    long = gps_all['GPSLongitude']
                    lat = gps_all['GPSLatitude']

                    print 'Filename = {}'.format(x)

                    lat_in_degrees = _convert_to_degress(lat)
                    if lat_ref == 'S':
                        lat_in_degrees = -abs(lat_in_degrees)

                    print 'Latitude = {}'.format(lat_in_degrees)

                    long_in_degrees = _convert_to_degress(long)
                    if long_ref == 'W':
                        long_in_degrees = -abs(long_in_degrees)
                    print 'Longitude = {}'.format(long_in_degrees)

                    shp_list.append([long_in_degrees, lat_in_degrees])
                    shape_creator()

                except:
                    print 'NO GPS DATA FOUND!! in {}'.format(x)
                    pass
            else:
                print 'Not a .jpg image..skipping \n'
            num += 1

        single_shape_creator()
        shp_list = []
        num2 += 1
    print 'DONE'


def shape_creator():

    pt_list = [[long_in_degrees, lat_in_degrees]]
    pt = arcpy.Point()
    ptGeoms = []
    for p in pt_list:
        pt.X = p[0]
        pt.Y = p[1]
        ptGeoms.append(arcpy.PointGeometry(pt))
    print 'Creating Shapefile from coordinates of {}...'.format(x)
    arcpy.CopyFeatures_management(ptGeoms, os.path.join(root, 'SHAPE{}.shp'.format(num)))

    print 'Shapefile sucessfully created!!! \n'

def single_shape_creator():

    pt = arcpy.Point()
    ptGeoms = []
    for p in shp_list:
        pt.X = p[0]
        pt.Y = p[1]
        ptGeoms.append(arcpy.PointGeometry(pt))
    print 'Creating Single Shapefile from all pictures in {}...'.format(root)
    arcpy.CopyFeatures_management(ptGeoms, os.path.join(root, 'INDIVIDUAL_SHAPE_{}.shp'.format(num2)))
    print 'Individual Shapefile sucessfully created!!! \n'


def _convert_to_degress(value):

    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

image_to_shp()


