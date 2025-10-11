import maya.cmds as cmds
import maya.mel as mel
import os
import threading

mas=[];
fbxs=[];
targetPatn=r"E:\Work\B12\Colossus-20201030\fbx";
for root,dirs,files in os.walk(r"E:\Work\B12\Colossus-20201030\maya"):
    for file in files:
        fileName=os.path.splitext(file);
        if  fileName[1]== '.ma':
            mas.append(os.path.join(root, file));
            fbxs.append(os.path.join(targetPatn,fileName[0]+".fbx"));
            
for index in range(len(mas)):
    cmds.file(mas[index], open=True,force=True);
    cmds.select("root");
    cmds.file(fbxs[index],es=True,f=True,type="FBX export");

