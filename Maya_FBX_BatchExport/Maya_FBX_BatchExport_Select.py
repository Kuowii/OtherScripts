import maya.cmds as cmds
import maya.mel as mel
import os
import threading

def ExportFileToFBX(sfile,ofile):
    try:
        cmds.file(sfile, open=True,force=True);
        cmds.file(ofile,ea=True,f=True,type="FBX export");
        return True
    except Exception as err:
        print(sfile+' error : '+str(err));
        return False

def DoBatchExport():
    files = cmds.fileDialog2(dialogStyle=2, fileMode=4, okCaption="Select Files To Export")
    folder = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption="Select Output Folder")[0]
    errfile = open(os.path.join(folder,'errfile.txt'), "w");
    errCount=0
    for fpath in files:
        fileName=os.path.splitext(os.path.basename(fpath));
        output=os.path.join(folder,fileName[0]+".fbx")
        isExport=ExportFileToFBX(fpath,output)
        if not isExport:
            errCount=errCount+1
            errfile.write(fpath+'\n')
            errfile.flush()
    errfile.close()
    cmds.confirmDialog( title='Wings Tool', message='Export Finish!\nError File:%d'%errCount, button=['OK'], defaultButton='OK', dismissString='No' )

DoBatchExport();