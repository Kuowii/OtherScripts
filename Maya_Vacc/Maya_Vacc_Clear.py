# -*- coding: utf-8 -*-
import maya.cmds as cmds
aa=cmds.ls();
isVir = False;
for a in aa:
    b=a.lower()
    if "vacc" in b:
        cmds.delete(a);
        isVir = True;
    if "breed" in b:
        cmds.delete(a);
        isVir = True;
    if "virus" in b:
        cmds.delete(a);
        isVir = True;
                
if isVir:
    cmds.file(modified=True)
    cmds.confirmDialog( title='Wings Tool', message="已清除脚本", button=['OK'], defaultButton='OK')
else:
    cmds.confirmDialog( title='Wings Tool', message="未感染", button=['OK'], defaultButton='OK')