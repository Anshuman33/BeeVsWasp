import os
import shutil
import pandas

def getPaths(labelsPath):
    '''
    Takes in the path of the labels.csv file and returns separate numpy arrays of 
    training, test and validation image paths with the first column being the path
    and second columns being the label.
    '''
    labelDf = pandas.read_csv(labelsPath)
    trainPaths = (labelDf.loc[(labelDf.is_validation==0) & (labelDf.is_final_validation == 0)][["path","label"]]).values
    valPaths = (labelDf.loc[(labelDf.is_validation==1) & (labelDf.is_final_validation == 0)][["path","label"]]).values
    testPaths = (labelDf.loc[(labelDf.is_validation==0) & (labelDf.is_final_validation == 1)][["path","label"]]).values
    return trainPaths,valPaths,testPaths

def copyImages(pathList,sourceBasePath,destPath,datasetType):
    '''
    pathList - List of image details containing the first column as path to image and the second columns being the label of the image.\n 
    basePath - folder where the folders for images are available\n
    destPath - folder where the images have to be stored classwise in folders\n
    type - specify whether data is for 'train', 'test' or 'val' set.
    '''
    destDir = os.path.join(destPath,datasetType)
    filesCopied = 0
    if not os.path.exists(destDir):
        os.mkdir(destDir)
    
    for record in pathList:
        source = os.path.join(sourceBasePath,record[0])
        classFolder = os.path.join(destDir,record[1])
        if not os.path.exists(classFolder):
            os.mkdir(classFolder)
        dest = os.path.join(classFolder,os.path.basename(record[0]))
        shutil.copyfile(source,dest)
        filesCopied+=1

    print("Copied {} images for {}.".format(filesCopied,datasetType))

labelsPath = "kaggle_bee_vs_wasp\\labels.csv"
trainPaths,valPaths,testPaths = getPaths(labelsPath)
sourceBasePath = "kaggle_bee_vs_wasp"
destPath = "dataset"

copyImages(trainPaths,sourceBasePath,destPath,"train")
copyImages(valPaths,sourceBasePath,destPath,"val")
copyImages(testPaths,sourceBasePath,destPath,"test")








