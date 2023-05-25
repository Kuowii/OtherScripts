# -*- coding: utf-8 -*-
#===============================================================================
# Command:    
# if you want to save weights,you can eval:
#    1. select one mesh
#    2. ly_exportWeight(__defaultFileName,__round)    
# if you want to import weights,you can:
#    1. select one mesh
#    2. ly_importWeight(__defaultFileName="",__round)
#
# 
#    __defaultFileName = "D:/weightFile.txt"
#    __round = 6
#
#
# Author:     liaoyong
# mail:       liaoyong@of3d.com
# telephone:  15850792079
# QQ:         274788920
# Department: OF3D gamesArtist technology department
#===============================================================================
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as mc
import os
import sys
import time
import linecache



#===============================================================================
# main GUI
#===============================================================================
def ly_IO_weightGUI_OF3D():
    GUI = 'ly_IOWeight_OF3D'
    if mc.window(GUI,exists=True):
        mc.deleteUI(GUI,window = True)
    mc.window(GUI,t='OF3D IO Weight',minimizeButton=0,maximizeButton=0,menuBar=1)

    mc.select(cl=True)

    form = mc.formLayout(numberOfDivisions=100)

    mc.scriptJob(e=["SelectionChanged","IOweight_LoadScriptJob()"], parent = GUI, replacePrevious=True)

    outputWeightButton = mc.button(l="Save Weight",c="ly_outFile_CMD_OF3D()")
    inputWeightButton = mc.button(l="Input Weight",c="ly_importFile_CMD_OF3D()")

    listFile = mc.columnLayout("setWeight",adj=1)
    mc.separator(h=20)
    mc.text(l="Please select 1 mesh",align='center',font="boldLabelFont")
    mc.rowColumnLayout(numberOfRows=1)
    mc.text('fileNameText',l='Output File:',align='center',font="boldLabelFont",w=80)
    mc.textField('fileNameList',text="",w=450)
    mc.setParent('..')
    mc.setParent('..')

    mc.setParent('..')

    mc.formLayout( form, edit=True, attachForm=[(outputWeightButton, 'top', 5),  (outputWeightButton, 'left', 5), (listFile, 'left', 5), (listFile, 'bottom', 5), (listFile, 'right', 5), (inputWeightButton, 'top', 5), (inputWeightButton, 'right', 5) ],attachControl=[(outputWeightButton, 'bottom', 5, listFile), (inputWeightButton, 'bottom', 5, listFile)],attachPosition=[(outputWeightButton, 'right', 5, 50), (inputWeightButton, 'left', 5, 50)],attachNone=(listFile, 'top') )

    mc.showWindow(GUI)

# selected changed
def IOweight_LoadScriptJob():
    try:
        USERNAME = os.environ["USERPROFILE"]
        USERNAME = USERNAME.split("\\")[2]

        objSel = mc.ls(sl=True,o=True)
        fileName = "C:/Users/" + USERNAME + "/Documents/maya/projects/default/data/" + objSel[0] + ".txt"
        #C:\Users\liaoyong\Documents\maya\projects\default\data
        mc.textField('fileNameList',e=True,text=fileName)
    except:
        pass

#===============================================================================
# CMD of output and import
#===============================================================================
def ly_outFile_CMD_OF3D():
    __defaultFileName = mc.textField('fileNameList',q=True,text=True)
    ly_exportWeight(__defaultFileName,6)
def ly_importFile_CMD_OF3D():
    __defaultFileName = mc.textField('fileNameList',q=True,text=True)
    ly_importWeight(__defaultFileName,6)


def __lyCreateInfNameList(skinClusterNode):
    """this function return out list containing joint name in ordered list as they are attached internally to skinCluster
    which are used when seting or getting weights from skincluster."""

    infNameList =[]
    infs = OpenMaya.MDagPathArray()
    numInfs = skinClusterNode.influenceObjects(infs)
    for counter in range(0,numInfs,1):
        infName = infs[counter].partialPathName()
        infNameList.append(infName)
    return infNameList


def __lyNormalizeWeight(weights,place,infNameList,addZero):
    """For the given weight list this func will normalize and round off the weights and
    provisionally could remove nonZero members.This func returns Dictionary with key as
    influenceObj and value as weights."""

    allWeight = 0
    largestWeight = 0
    heavyJnt =""
    nonZeroDict={}
    for i in range(0,len(weights),1):
        if (weights[i] != 0):
            weights[i]= round(weights[i],4)
        nonZeroDict[infNameList[i]] = weights[i]
        if (largestWeight < nonZeroDict[infNameList[i]]):
            largestWeight = nonZeroDict[infNameList[i]]
            heavyJnt = infNameList[i]
        allWeight += nonZeroDict[infNameList[i]]
    remWeight = 1 - allWeight
    nonZeroDict[heavyJnt] = nonZeroDict[heavyJnt] + remWeight
    if addZero == 0:
        clearList=[]
        for each in nonZeroDict.keys():
            if nonZeroDict[each] == 0:
                #nonZeroDict.pop(each)
                clearList.append(each)
        for ec in clearList:
            nonZeroDict.pop(ec)
    return nonZeroDict


# re- skin oject
def ly_reSkinObj(__defaultFileName=""):
    # get inlfuences
    _infs = linecache.getline(__defaultFileName,3)
    _infs = _infs.split(" ")
     
    _selList  = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(_selList)
    
    if _selList.length() != 1:
        OpenMaya.MGlobal.displayError("Nothing selected")
    
    _MObject = OpenMaya.MObject()
    _DagPath = OpenMaya.MDagPath()
    
    _selList.getDagPath(0,_DagPath)
    _selList.getDependNode(0,_MObject)
    
    if _DagPath.apiType() != 295 and _DagPath.apiType() != 294 and _DagPath.apiType() != 110:
        OpenMaya.MGlobal.displayError("Please select Polygon object, or vertices to save weights")
    
    _skinCluster = ""
    #for _skinCluster in mc.listHistory(_DagPath.partialPathName(),f=0,bf=1):
    for _skinCluster in mc.listHistory(_DagPath.partialPathName(), interestLevel = 1, pruneDagObjects = True):
        if mc.nodeType(_skinCluster) == 'skinCluster':
            break
    mc.delete(_skinCluster)    
    __returnArray = []
    _selList.getSelectionStrings(__returnArray)
    
    mc.select(cl=True)
    mc.skinCluster(_infs,__returnArray[0],normalizeWeights=1,maximumInfluences=1,obeyMaxInfluences=0,toSelectedBones=True,removeUnusedInfluence=0,)
    mc.select(__returnArray[0],r=True)



#===============================================================================
# write weight
#===============================================================================
def ly_exportWeight(__defaultFileName="",__round=6):
    """
    __defaultFileName = "C:/Users/liaoyong/Documents/maya/projects/default/data/pasted__body.txt"
    ly_exportWeight(__defaultFileName,6)
    """
    startTime = time.time()
    
    _selList  = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(_selList)
    
    if _selList.length() != 1:
        OpenMaya.MGlobal.displayError("Nothing selected")
    
    _MObject = OpenMaya.MObject()
    _DagPath = OpenMaya.MDagPath()
    
    _selList.getDagPath(0,_DagPath)
    _selList.getDependNode(0,_MObject)
    
    if _DagPath.apiType() != 295 and _DagPath.apiType() != 294 and _DagPath.apiType() != 110:
        OpenMaya.MGlobal.displayError("Please select Polygon object, or vertices to save weights")
    
    _skinCluster = ""
    for _skinCluster in mc.listHistory(_DagPath.partialPathName(), interestLevel = 1, pruneDagObjects = True):
        if mc.nodeType(_skinCluster) == 'skinCluster':
            break
    
    OpenMaya.MGlobal.getSelectionListByName( _skinCluster,_selList)
    _skinObj = OpenMaya.MObject()
    _selList.getDependNode(1, _skinObj )
    
    _infNameList = []
    _skinClusterNode = OpenMayaAnim.MFnSkinCluster(_skinObj)
    _infNameList = __lyCreateInfNameList(_skinClusterNode)
    
    
    # writes out skin weights to ascii format.
    __fileName = __defaultFileName
    #f = open(__fileName,'wb')
    f = open(__fileName,'w')
    f.write('#saving weights....\n')
    _exportFile = ""
    _exportFile += "# Joint List\n"
    _exportFile += " ".join(_infNameList)
    _exportFile += "\n# Joint list ends\n"
    f.write(_exportFile)
    f.write("# skin weight begins\n")
    
    OpenMaya.MGlobal.displayInfo("export weight...")
    vertIter = OpenMaya.MItGeometry(_MObject)
    while not vertIter.isDone():
        infCount = OpenMaya.MScriptUtil()
        infCountPtr = infCount.asUintPtr()
        OpenMaya.MScriptUtil.setUint(infCountPtr,0)
        weights = OpenMaya.MDoubleArray()
        
        _skinClusterNode.getWeights(_DagPath, vertIter.currentItem(), weights, infCountPtr)
        weightDict = __lyNormalizeWeight(weights,__round,_infNameList,0)
        _exportFile = "".join('['+str(vertIter.index())+']')
        _exportFile += "\n"
        _exportFile += " ".join(weightDict.keys())
        _exportFile += "\n"
    
        for eachVal in weightDict.values():
            _exportFile += str(eachVal) + " "
        _exportFile += "\n"
        f.write(_exportFile)
        vertIter.next()
    
    f.write("#end of skinWeight data")
    f.close()
    # end time
    endTime = time.time()
    allTime = endTime-startTime
    OpenMaya.MGlobal.displayInfo("programming time:"+str(allTime)+":  save successfully")



def ly_importWeight(__defaultFileName="",__round=6):
    """
     __defaultFileName = "C:/Users/liaoyong/Documents/maya/projects/default/data/pasted__body.txt"
     ly_importWeight(__defaultFileName,6)
    """
    startTime = time.time()
    
    ####
    _selList  = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(_selList)
    
    if _selList.length() != 1:
        OpenMaya.MGlobal.displayError("Nothing selected")
    
    _MObject = OpenMaya.MObject()
    _DagPath = OpenMaya.MDagPath()
    
    _selList.getDagPath(0,_DagPath)
    _selList.getDependNode(0,_MObject)
    
    if _DagPath.apiType() != 295 and _DagPath.apiType() != 294 and _DagPath.apiType() != 110:
        OpenMaya.MGlobal.displayError("Please select Polygon object, or vertices to save weights")
    
    # get skincluster
    _skinCluster = ""
    for _skinCluster in mc.listHistory(_DagPath.partialPathName(),interestLevel = 1, pruneDagObjects = True):
        if mc.nodeType(_skinCluster) == 'skinCluster':
            break
    
    OpenMaya.MGlobal.getSelectionListByName( _skinCluster,_selList)
    _skinObj = OpenMaya.MObject()
    _selList.getDependNode(1, _skinObj )
    
    # check influence
    _infNameList = []
    _skinClusterNode = OpenMayaAnim.MFnSkinCluster(_skinObj)
    _infNameList = __lyCreateInfNameList(_skinClusterNode)
    #===========================================================================
    # for i in _infNameList:
    #    mc.setAttr(i+".liw",0)
    #===========================================================================
    __returnArray = []
    _selList.getSelectionStrings(__returnArray)
    selStrComp = mc.polyListComponentConversion (__returnArray[0],ff=1,fe=1,fuv=1,fvf=1,fv=1,tv=1) #ADD vertex to sel list
    mc.select(selStrComp,r=1)
    OpenMaya.MGlobal.getActiveSelectionList(_selList)
    mc.select(__returnArray,r=1)
    _MObjectComp = OpenMaya.MObject()
    _selList.getDagPath(0,_DagPath,_MObjectComp)
    

    #zero out all the weights to supress error message
    eachVertImport = OpenMaya.MObject()
    weights = OpenMaya.MDoubleArray()
    __indArrayUndo= OpenMaya.MIntArray()
    __unDoWeights = OpenMaya.MDoubleArray() 
    __indArrayImport= OpenMaya.MIntArray()
    for i in range(0,len(_infNameList),1):
        __indArrayUndo.append(i)
        weights.append(0)
    
    _skinClusterNode.setWeights(_DagPath,_MObjectComp,__indArrayUndo,weights,False,__unDoWeights)
    weights.clear()
    __indArrayImport.clear() 
    
    # writes out skin weights to ascii format.
    __fileName = __defaultFileName
    try:
        fRead = open(__fileName,'r')
        
    except:
        OpenMaya.MGlobal.displayError('file '+ __fileName +'does not exist')
    skinWtData = 0
    for line in fRead:
        if line.find('# skin weight begins') != -1:
            skinWtData = 1
            break
    if skinWtData == 0:
        OpenMaya.MGlobal.displayError("skin weights data not found in given file") 

    ###
    allVtxDict = {}
    for line in fRead:
        if line.find("#end of skinWeight data") != -1: break
        dictVtxKey = line[1:-2] # removes [] #make sure data [] matches correctly at this point
        #ValJntList = fRead.next().split()
        #valWtList = fRead.next().split()
        ValJntList=next(fRead).split()
        valWtList=next(fRead).split()
        allVtxDict[dictVtxKey] = [ValJntList,valWtList]
    fRead.close()   
     
    #===========================================================================
    # import weight beginning
    #===========================================================================   
    vertIter = OpenMaya.MItGeometry(_MObject)
    while not vertIter.isDone():
        vNumb = str(vertIter.index())
        infName = allVtxDict[vNumb][0]
        weightsString = allVtxDict[vNumb][1]
        for i in range(len(weightsString)):
            weights.append(float(weightsString[i]))
            __indArrayImport.append(_infNameList.index(infName[i]))
    
        _skinClusterNode.setWeights(_DagPath,vertIter.currentItem(),__indArrayImport,weights,False)
        vertIter.next()
        weights.clear()
        __indArrayImport.clear()
        
    
    # end time
    endTime = time.time()
    allTime = endTime-startTime
    OpenMaya.MGlobal.displayInfo("programming time:"+str(allTime)+":  save successfully")
ly_IO_weightGUI_OF3D()