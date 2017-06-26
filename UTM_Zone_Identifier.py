### Takes points and projects them based on the UTM zone they're in

import arcpy
import os

arcpy.env.overwriteOutput = True

world_cities = r'F:\Files\GIS\scripts\utm_project\resources\World_Cities.shp'
utm_zones = r'F:\Files\GIS\scripts\utm_project\resources\UTM_Zone_Boundaries.shp'
outputs = r'F:\Files\GIS\scripts\utm_project\resources\outputs'

northern_hem_codes = {1: 32601, 2: 32602, 3: 32603, 4: 32604, 5: 32605, 6: 32606, 7: 32607, 8: 32608, 9: 32609, 10: 32610,
                      11: 32611, 12: 32612, 13: 32613, 14: 32614, 15: 32615, 16: 32616, 17: 32617, 18: 32618, 19: 32619,
                      20: 32620, 21: 32621, 22: 32622, 23: 32623, 24: 32624, 25: 32625, 26: 32626, 27: 32627, 28: 32628,
                      29: 32629, 30: 32630, 31: 32631, 32: 32632, 33: 32633, 34: 32634, 35: 32635, 36: 32636, 37: 32637,
                      38: 32638, 39: 32639, 40: 32640, 41: 32641, 42: 32642, 43: 32643, 44: 32644, 45: 32645, 46: 32646,
                      47: 32647, 48: 32648, 49: 32649, 50: 32650, 51: 32651, 52: 32652, 53: 32653, 54: 32654, 55: 32655,
                      56: 32656, 57: 32657, 58: 32658, 59: 32659, 60: 32660}

southern_hem_codes = {1: 32701, 2: 32702, 3: 32703, 4: 32704, 5: 32705, 6: 32706, 7: 32707, 8: 32708, 9: 32709, 10: 32710,
                      11: 32711, 12: 32712, 13: 32713, 14: 32714, 15: 32715, 16: 32716, 17: 32717, 18: 32718, 19: 32719,
                      20: 32720, 21: 32721, 22: 32722, 23: 32723, 24: 32724, 25: 32725, 26: 32726, 27: 32727, 28: 32728,
                      29: 32729, 30: 32730, 31: 32731, 32: 32732, 33: 32733, 34: 32734, 35: 32735, 36: 32736, 37: 32737,
                      38: 32738, 39: 32739, 40: 32740, 41: 32741, 42: 32742, 43: 32743, 44: 32744, 45: 32745, 46: 32746,
                      47: 32747, 48: 32748, 49: 32749, 50: 32750, 51: 32751, 52: 32752, 53: 32753, 54: 32754, 55: 32755,
                      56: 32756, 57: 32757, 58: 32758, 59: 32759, 60: 32760}


def utm_zone_identifier():

    arcpy.MakeFeatureLayer_management(utm_zones, 'utm_zones_layer')

    with arcpy.da.SearchCursor(world_cities, ['SOV0NAME', 'NAME', 'LATITUDE', 'LONGITUDE', 'FID']) as cities_cursor:
        for x in cities_cursor:
            print 'Country name = {}'.format(x[0])
            print 'City name = {}'.format(x[1])
            single_city_name = x[1]

            for replace in ["'", "-", " "]:
                if replace in single_city_name:
                    single_city_name = single_city_name.replace(replace, "_")
                    print '{} needed to be edited because {} was found'.format(x[1], replace)

            arcpy.MakeFeatureLayer_management(world_cities, single_city_name, """ FID = {} """.format(x[4]))
            arcpy.SelectLayerByLocation_management('utm_zones_layer', 'INTERSECT', single_city_name)

            with arcpy.da.SearchCursor('utm_zones_layer', ['ZONE', 'HEMISPHERE']) as utm_cursor:
                for y in utm_cursor:
                    utm_value = y[0]
                    hemisphere_value = y[1]
                    print 'The UTM Zone for {} = {}'.format(single_city_name, utm_value)
                    print 'The Hemisphere Value for {} = {}'.format(single_city_name, hemisphere_value)

                    if hemisphere_value == 'n':
                        utm_value_int = int(utm_value)
                        north_spatial_ref = northern_hem_codes[utm_value_int]
                        print 'The Spatial Reference code for {} is {} \n'.format(single_city_name, north_spatial_ref)
                        arcpy.Project_management(single_city_name, os.path.join(outputs, single_city_name + '_UTM_Projection.shp'), north_spatial_ref)

                    elif hemisphere_value == 's':
                        utm_value_int = int(utm_value)
                        south_spatial_ref = southern_hem_codes[utm_value_int]
                        print 'The Spatial Reference code for {} is {} \n'.format(single_city_name, south_spatial_ref)
                        arcpy.Project_management(single_city_name, os.path.join(outputs, single_city_name + '_UTM_Projection.shp'), south_spatial_ref)

utm_zone_identifier()