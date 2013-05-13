import arcpy, os, convertGlacierData.convertXyznToPolyline

sourceLayer = arcpy.GetParameter(0)

descSourceLayer = arcpy.Describe(sourceLayer)
extension = descSourceLayer.extension.split("_")

if len(extension) != 2:
    arcpy.AddMessage("Chosen layer is not an event layer. Tool will stop!")
elif len(extension) == 2:
    if extension[1] == "Features":
        arcpy.AddMessage("Chosen layer is an event layer. Tool will start!")

        # Reading the source file name and path
        eventFileName = os.path.join(descSourceLayer.path, descSourceLayer.baseName + "." + extension[0])
        arcpy.AddMessage("Source file: " + eventFileName)

        convertedShapeFile = convertGlacierData.convertXyznToPolyline.doConversion(eventFileName)
        arcpy.AddMessage("Shapefile created: " + convertedShapeFile)

        # Adding the newly created shapefile on top.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        newlayer = arcpy.mapping.Layer(convertedShapeFile)
        arcpy.mapping.AddLayer(df, newlayer, "TOP")
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        
        del mxd, df, newlayer
        
    else:
        arcpy.AddMessage("Chosen layer is not an event layer. Tool will stop!")
