# Script that counts number of feature classes, number of features in each feature class and total number of features in database
# Also creates bar graph

import arcpy, time, datetime
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

program_start = datetime.datetime.now().time()
start_time = time.time()
print 'Program started at', program_start, '\n'

# ENTER PATH TO YOUR GEODATABASE
ws = arcpy.env.workspace = r'F:\Files\GIS\OSM_data\Philadelphia_Metro_Area_OSM.gdb'
fc_list = arcpy.ListFeatureClasses()

fc_count = 0
fc_count_list = []

for x in fc_list:
    with arcpy.da.SearchCursor(x, ['osm_id']) as count_cursor:
        for record in count_cursor:
            fc_count += 1
        fc_count_list.append(fc_count)
        fc_count = 0

fc_count_dict = dict(zip(fc_list, fc_count_list))

print 'There are', len(fc_list), 'feature classes in the database \n'

for k, v in sorted(fc_count_dict.items()):
    print 'Feature Class:', k, '\n' + 'Number of features:', v, '\n'

print 'There are', sum(fc_count_dict.itervalues()), 'total features in the database \n'
print 'Creating graph...'

font_size = 10
plt.figure(figsize=(22,10))

new_list = len(fc_count_list)

plt.bar(range(new_list), fc_count_list, width=2.0, align='center')

plt.xticks(range(new_list), fc_list, rotation='vertical', fontsize=font_size)
#plt.yticks(fc_count_list)
plt.xlabel('Feature Class Name')
plt.ylabel('Feature Count')
plt.title('Feature Class Counter')
plt.legend

'''for a,b in zip(list(range(70)), fc_count_list):
    plt.text(a, b, str(b), rotation='45')'''

plt.subplots_adjust(left=0.12, bottom=0.29, right=0.90, top=0.90, wspace=0.20, hspace=0.20)
plt.show()

print("Program took --- %s seconds --- to complete" % (time.time() - start_time))

