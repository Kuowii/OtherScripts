# -*- coding: utf-8 -*-
from maya import cmds
bones=cmds.ls(sl=1)
for b in bones:
    attrn=b+".translate";
    tp=cmds.getAttr(attrn)[0];
    cmds.setAttr(attrn+"X",round(tp[0], 3))
    cmds.setAttr(attrn+"Y",round(tp[1], 3))
    cmds.setAttr(attrn+"Z",round(tp[2], 3))
cmds.confirmDialog( title='Compelet', message='Bone Translate Clip Finish!')