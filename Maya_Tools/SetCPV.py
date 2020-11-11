# 修改顶点色

import maya.cmds as cmds
selected = cmds.ls(sl=True,long=True);
cmds.polyColorPerVertex( rgb=(0,0,0) )