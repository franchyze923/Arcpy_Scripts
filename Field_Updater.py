# Updates all records that have 'null' value in the 'name' and 'maxspeed' fields.

import arcpy, time, datetime

program_start = datetime.datetime.now().time()
start_time = time.time()
print 'Program started at ', program_start

# ENTER PATH TO YOUR GEODATABASE
ws = arcpy.env.workspace = r'F:\Files\GIS\OSM_data\Philadelphia_Metro_Area_OSM.gdb'
fc_list = arcpy.ListFeatureClasses()

# Enter fields you want to look through
field_1 = 'name'
field_2 = 'maxspeed'

# Enter values you would like to update/change
values_to_update = ['null', '<null>', '<Null>', 'Null', None]

field_1_count = 0
field_2_count = 0
updated1 = 0
updated2 = 0

for fc in fc_list:
    print fc
    field_list = []
    fields = arcpy.ListFields(fc)

    for field in fields:
        print field.name
        field_list.append(field.name)
    #print [y.encode('ascii') for y in field_list]

    if field_1 in field_list:
        field_1_count += 1
        print field_1, 'is in ', fc
        with arcpy.da.UpdateCursor(fc, [field_1]) as field_cursor:
            for x in field_cursor:
                if x[0] in values_to_update:
                    updated1 += 1
                    print 'This record needs to be updated. Updating...'
                    # WHAT YOU WANT THE NEW VALUE TO BE
                    x[0] = 'UPDATED_1'
                    print 'Updated record to ', x[0]
                    field_cursor.updateRow(x)
                else:
                    print 'Nothing to update'
    else:
        print field_1, 'is not in ', fc

    if field_2 in field_list:
        field_2_count += 1
        print field_2,  'is in ', fc
        with arcpy.da.UpdateCursor(fc, [field_2]) as field_cursor:
                for x in field_cursor:
                    if x[0] in values_to_update:
                        updated2 += 1
                        print 'This record needs to be updated. Updating...'
                        # WHAT YOU WANT THE NEW VALUE TO BE
                        x[0] = 'UPDATED_2'
                        print 'Updated record to ', x[0]
                        field_cursor.updateRow(x)
                    else:
                        print 'Nothing to update'
    else:
        print field_2, 'is not in ', fc

print 'Total number of feature classes that had ' + '"{}"'.format(field_1) + ' field =', field_1_count
print 'Total number of records that needed to be updated in ' + '"{}"'.format(field_1) + ' field =', updated1

print 'Total count of feature classes that had ' + '"{}"'.format(field_2) + ' field =', field_2_count
print 'Total number of records that needed to be updated in ' + '"{}"'.format(field_2) + ' field =', updated2

print("Program took --- %s seconds --- to complete" % (time.time() - start_time))
