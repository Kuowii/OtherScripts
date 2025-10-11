import maya.cmds as cmds
import maya.mel as mel
import os
import threading

keys=[]
option='precision=17;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=0:10;options=keys;hierarchy=below;controlPoints=0;shapes=1;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy below -controlPoints 0 -shape 1 '
KeyWord = 'C_Reference'

def SelectNodeByKeyword(kw):
    nodes = cmds.ls(type='transform')
    for node in nodes:
        if kw in node:
            return node
    return null

def ExportFileToAnim(sfile,ofile):
    try:
        cmds.file(sfile, open=True,force=True);
    except Exception as err:
        print(sfile+' Open Exception : '+str(err)); 
    try:
        node = SelectNodeByKeyword(KeyWord)
        cmds.select(node)
    except Exception as err:
        print(sfile+' Scene Exception : '+str(err));
    try:
        cmds.file(ofile,es=True,f=True,type="animExport",op=option);
        return True
    except Exception as err:
        print(sfile+' Export Exception : '+str(err));
        return False

def DoBatchExport():
    files = cmds.fileDialog2(dialogStyle=2, fileMode=4, okCaption="Select Files To Export")
    folder = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption="Select Output Folder")[0]
    errfile = open(os.path.join(folder,'errfile.txt'), "w");
    errCount=0
    if files == None or len(files)<=0 or folder == None or not folder :
        cmds.confirmDialog( title='Wings Tool', message='No files selected!', button=['OK'], defaultButton='OK', dismissString='No' )
        return
    for fpath in files:
        fileName=os.path.splitext(os.path.basename(fpath));
        output=os.path.join(folder,fileName[0]+".anim")
        isExport=ExportFileToAnim(fpath,output)
        if not isExport:
            errCount=errCount+1
            errfile.write(fpath+'\n')
            errfile.flush()
    errfile.close()
    cmds.confirmDialog( title='Wings Tool', message='Export Finish!\nError File:%d'%errCount, button=['OK'], defaultButton='OK', dismissString='No' )

DoBatchExport();