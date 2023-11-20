#1.Update webapp builder configuration when webmap changed in same environment
#2.Update webapp builder configuration from development environment to test/prod/preprod etc.

import arcpy
import fileinput
from os import walk
import glob
from IPython.display import display
import arcgis
from arcgis.gis import GIS
from arcgis.mapping import WebMap
import datetime
import operator


# COR_RO_LANDSEARCH COR_RO_UNITED
# Configuration values
#
portlsource='https://dv-gis.dev.southernwater.co.uk/portal'
portltarget='https://tt-gis.dev.southernwater.co.uk/portal'
surl='https://dv-gis.dev.southernwater.co.uk/portal'
turl='https://tt-gis.dev.southernwater.co.uk/portal'
swebmapid='2e8831cfd9e143fc9aa179eb52c585d7'
twebmapid='0e924d95f83341db835973748409c51a'
gissource = GIS(portlsource,'adm_MekasrR@DEV','JYMY64zd')
gistarget = GIS(portltarget,'adm_MekasrR@DEV','JYMY64zd')
swebmap = "COR_RO_UNITED"
twebmap = "COR_RO_UNITED"
dir_path = r'E:\CyientUsers\SriRam\Singleconfig\**\*.json'
# End Configuration values - replace above variables with values



#Class for dictnery
class create_dict(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value



#start Process area
# Read  data        
replacetexts = create_dict()
replacetexts.add(portlsource, portltarget)
replacetexts.add(surl, turl)
replacetexts.add(swebmapid, twebmapid)
now = datetime.datetime.now()
print("Start time : " + now.strftime('%Y-%m-%d %H:%M:%S'))
y=0



#Read webmap 1
webmap_searchsource = gissource.content.search(swebmap, item_type="Web Map",max_items=100)
for item in webmap_searchsource:
     item_title = item.title
     print(item_title)
     map_itemsource=""
     if item_title == swebmap:
         map_itemsource = item
print(map_itemsource)
item_datasource = map_itemsource.get_data()
sourcelayers=[]
sourceids=[]
for index, i in enumerate(item_datasource["operationalLayers"]):
            ## get the name of the layer
            title = item_datasource["operationalLayers"][index]["title"]
            idval = item_datasource["operationalLayers"][index]["id"]
            sourcelayers.append(title)
            sourceids.append(idval)



#Read webmap 2
webmap_searchtarget = gistarget.content.search(twebmap, item_type="Web Map",max_items=100)
for item in webmap_searchtarget:
     item_title = item.title
     if item_title == twebmap:
         map_itemtarget = item
print(map_itemtarget)
item_datatarget = map_itemtarget.get_data()
targetlayers=[]
targetids=[]
for index, i in enumerate(item_datatarget["operationalLayers"]):
            ## get the name of the layer
            title = item_datatarget["operationalLayers"][index]["title"]
            tidval = item_datatarget["operationalLayers"][index]["id"]
            targetlayers.append(title)
            targetids.append(tidval)
            if sourcelayers.count(title) > 0:
               pogval=sourcelayers.index(title)
               replacetexts.add(sourceids[pogval], tidval)




#Replace config json with values and ids
for file in glob.glob(dir_path, recursive=True):
    print(file)
    x=0
    for line in fileinput.input(file ,inplace=True):
        #for searchtext in replacetexts:
        for searchtext, replacetext in replacetexts.items():
            #replacetext = replacetexts[searchtext]
            #print(searchtext)
            #print(replacetext)
            if(searchtext in line):
               line=line.replace(searchtext,replacetext)
               x = operator.add(x, 1)
               y = operator.add(y, 1)
        print(line, end='')
    #rtxt="Replaced " + x    
    print("Replaced :" + str(x))
#End Process area




#Print results   
print("Total Replaced :" + str(y))     
now = datetime.datetime.now()
print("End time : " + now.strftime('%Y-%m-%d %H:%M:%S'))





