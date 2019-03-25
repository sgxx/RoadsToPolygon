# coding=utf-8

import arcpy, time, os, traceback,datetime
import winsound

def deleteFeature(feature, f):
    if arcpy.Exists(feature):
        print 'delete flayer', feature
        print >> f, 'delete flayer', feature
        arcpy.Delete_management(feature)

if __name__ == '__main__':
    flayer = arcpy.GetParameterAsText(0)
    polygonFinalLayer = arcpy.GetParameterAsText(1)

    f = open(r'D:\new.txt', 'w+')

    try:
        filePath = os.path.dirname(flayer)
        arcpy.env.workspace = filePath
        if ".shp" in flayer:
            polylineLayer = filePath + '\\polyline999.shp'
            polygonLayerMid2 = filePath + '\\polygon999mid2.shp'
        else:
            polylineLayer = filePath + '\\polyline999'
            polygonLayerMid2 = filePath + '\\polygon999mid2'

        t_start = time.clock()

        spatial_ref = arcpy.Describe(flayer).spatialReference

        deleteFeature(polylineLayer,f)
        deleteFeature(polygonLayerMid2,f)

        print 'min', datetime.datetime.now()
        arcpy.MinimumBoundingGeometry_management(flayer, polylineLayer,"CONVEX_HULL")
        print 'buffer', datetime.datetime.now()
        arcpy.Buffer_analysis(polylineLayer, polygonLayerMid2,"5000 METERS", method="GEODESIC")
        print 'dissolve', datetime.datetime.now()
        arcpy.Dissolve_management(polygonLayerMid2, polygonFinalLayer, multi_part="SINGLE_PART")
        print 'general',datetime.datetime.now()
        arcpy.Generalize_edit(polygonFinalLayer, "5000 METERS")

        deleteFeature(polylineLayer, f)
        deleteFeature(polygonLayerMid2, f)

        winsound.Beep(500, 1000)

        t_end = time.clock()
        print 'Processing cost {} seconds'.format(t_end - t_start)

    except:
        print traceback.format_exc()
        print >> f, traceback.format_exc()

