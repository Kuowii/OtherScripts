import maya.cmds as cmds
import maya.mel as mel
import os
import threading

keys=[]
nodes=['em1700_golem_RIG:C_Reference','pc0100_luke_RIG:C_Reference']

def select_all_descendants(root_nodes):
    sel=[]
    for root_node in root_nodes:
        if not cmds.objExists(root_node):
            cmds.warning(f"Node {root_node} does not exist.")
            continue
        sel.append(root_node)
        descendants = cmds.listRelatives(root_node, allDescendents=True, fullPath=True)
        if descendants:
            sel= sel + descendants
    cmds.select(sel)

def delete_namespace(root_nodes):
    new_rootNames=[]
    for root_node in root_nodes:
        names = root_node.split(':')
        if len(names)>1:
            try:
                cmds.namespace( rm=names[0],mnr=True)
            except:
                pass
            new_rootNames.append(names[1])
        else:
            new_rootNames.append(root_node)
    return new_rootNames

def ExportFileToFBX(sfile,ofile):
    try:
        cmds.file(sfile, open=True,force=True);
    except Exception as err:
        print(sfile+' Open Exception : '+str(err)); 
    try:
        new_nodes=delete_namespace(nodes)
        select_all_descendants(new_nodes)
    except Exception as err:
        print(sfile+' Scene Exception : '+str(err));
    try:
        cmds.file(ofile,es=True,f=True,type="FBX export");
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
    global nodes
    nodes = nodes+cmds.ls(sl=1)
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