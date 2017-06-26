import arcpy
arcpy.env.workspace = r'F:\Files\GIS\Other\Run_Keeper_Routes\gpx_files'
arcpy.env.overwriteOutput = True

endlocation = r'F:\Files\GIS\Other\Run_Keeper_Routes\shp_Files'

gpxlist = arcpy.ListFiles('*gpx')

for x in gpxlist:

    xdesc =arcpy.Describe(x)
    print(x)
    print('Converting', x, 'To a ShapeFile!')
    arcpy.GPXtoFeatures_conversion(x, endlocation + xdesc.basename)




