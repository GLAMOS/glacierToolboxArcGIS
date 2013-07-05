'''
Created on 05.07.2013

@author: yvow
'''

import os, arcpy

__OmegaPhiKappaLine = "OPK_LSR"
__XYZLine = "LSR_CAMERA"
__ImageID = "IMAGE_ID"

__DELIMITER = ","

__HEADER_IMAGE_ID = "ImageId"
__HEADER_PP_X = "X"
__HEADER_PP_Y = "Y"
__HEADER_PP_Z = "Z"
__HEADER_ROTATION_OMEGA = "Omega"
__HEADER_ROTATION_PHI = "Phi"
__HEADER_ROTATION_KAPPA = "Kappa"



def doExport(inputDirectory, exportFile):
    
    filesInDir = os.listdir(inputDirectory)
    for fileInDir in filesInDir:
        
        fileName = os.path.basename(fileInDir)
       
        arcpy.AddMessage("File found: " + fileName)
        
        exteriorParameters = getExteriorParameters(os.path.join(inputDirectory, fileInDir))
        
        arcpy.AddMessage("Parameters found: " + str(exteriorParameters))
        
        writeExteriorParameters(exportFile, exteriorParameters)
        
def writeHeader(exportFile):
    pass
        
def writeExteriorParameters(exportFile, exteriorParameters):
    
    f = open(exportFile, 'a')
    
    for i in range(len(exteriorParameters)):
        f.write(exteriorParameters[i])
        
        if i < len(exteriorParameters) - 1:
            f.write(__DELIMITER)
    
    f.write("\n")
    
    f.close()

def getExteriorParameters(supFile):
    f = open(supFile, 'r')
    
    # Getting the results ready
    imageId = ""
    ppX = ""
    ppY = ""
    ppZ = ""
    rotationOmega = ""
    rotationPhi = ""
    rotationKappa = ""
    
    for line in f:
        
        lineSpilt = line.split(" ")
        
        if lineSpilt[0] == __ImageID:
            imageId = lineSpilt[1].strip()
               
        if lineSpilt[0] == __OmegaPhiKappaLine:           
            rotationOmega = lineSpilt[1].strip()
            rotationPhi = lineSpilt[2].strip()
            rotationKappa = lineSpilt[3].strip()
        
        if lineSpilt[0] == __XYZLine:
            ppX = lineSpilt[1].strip()
            ppY = lineSpilt[2].strip()
            ppZ = lineSpilt[3].strip()
            
    return [imageId, ppX, ppY, ppZ, rotationOmega, rotationPhi, rotationKappa]