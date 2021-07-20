# -*- coding: utf-8 -*-
import maya.cmds as cmds;
import AntiVir;

print("Anti Vacc By Wings");
job = cmds.scriptJob(e=["SceneOpened",AntiVir.AntiVacc.clearVacc],per=True);