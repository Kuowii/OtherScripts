import sys
sys.path.append("C:/FPlus_Toolkit")

import maya.cmds as cmds
import FBX_Exporter_UI as exp

def checkGrpTrisCount(grpName, *args):
	global trisCount_ErrorMessage
	trisCount_ErrorMessage = ""

def main():
    exp.checkGrpTrisCount = checkGrpTrisCount;
    root_nodes = [obj for obj in cmds.ls(type='transform') if cmds.listRelatives(obj, parent=True) is None and not cmds.listRelatives(obj, children=True, shapes=True)]
    for obj in root_nodes:
        cmds.setAttr(obj + ".rotateY", 90)
        cmds.makeIdentity(obj, apply=True,r=1 ) 
    exp.exportSelectedOutputGrp(True,False, exp.folder_Scene, exp.folder_p4_Scene, exp.folder_export_Scene)