# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os
import threading
import codecs
from shutil import copyfile

def spAll():
    theNodes = cmds.ls(dag = True, s = True,type="shape");
    for n in theNodes:
        try:
            cmds.polySeparate(n);
        except:
            print(n + " separate fail.");

def setMat(f,dird):
    theNodes = cmds.ls(dag = True, s = True,type="shape");
    mb=cmds.ls(type='shadingEngine');
    fss=cmds.ls(type='file');
    for n in theNodes:
        print(n);
        shadeEng = cmds.listConnections(n , type = "shadingEngine");
        materials = cmds.ls(cmds.listConnections(shadeEng ), materials = True);
        for m in materials:
            print(m);
            if m.startswith('bl_'):continue;
            nBlinn = 'bl_'+m;
            sg = nBlinn+'_SG';
            if nBlinn not in mb:
                se = newNormalMat(m,fss,dird);
                nBlinn = se[0];
                sg = se[1];
                mb.append(nBlinn);
            cmds.select(cl=True);       
            cmds.select(n);
            cmds.hyperShade( nBlinn, assign=sg );
    print("Set Over " + f);

def newNormalMat(m,fss,dird):
    nBlinn = 'bl_'+m;
    sg = nBlinn+'_SG';
    nBlinn = cmds.shadingNode('blinn', asShader=True,n=nBlinn);
    sg=cmds.sets(renderable=1,noSurfaceShader=1,empty=1,name=nBlinn+'_SG');
    cmds.connectAttr( nBlinn + ".outColor",sg + ".surfaceShader",force=1);
    bc = m.replace("_mt", "_b");
    bn = m.replace("_mt","_n");
    mro = m.replace("_mt","_mro");
    
    if bc in fss:
        cmds.connectAttr(bc+'.outColor',nBlinn+'.color', force=True);
        currentFile = cmds.getAttr("%s.fileTextureName" % bc);
        copyfile(currentFile, dird+"\\"+bc+".tif");
    else: 
        print(bc+" not found.");
    
    if bn in fss:
        cmds.connectAttr(bn+'.outColor',nBlinn+'.normalCamera', force=True);
        currentFile = cmds.getAttr("%s.fileTextureName" % bn);
        copyfile(currentFile, dird+"\\"+bn+".tif");
    else: 
        print(bn+" not found.");
        
    if mro in fss:
        currentFile = cmds.getAttr("%s.fileTextureName" % mro);
        copyfile(currentFile, dird+"\\"+mro+".tif");
    else: 
        print(mro+" not found.");
    
    return [nBlinn,sg];

index_file = cmds.fileDialog2(fileFilter="*.txt",caption="选择目录文件",fm=1);
save_folder = cmds.fileDialog2(caption="选择输出目录",fm=3)[0];

#f=open(index_file[0], 'r', encoding='utf-8');

filelist = None;

from io import open
with open(index_file[0], 'r', encoding='utf-8') as f:
    filelist=f.readlines();

#filelist=f.readlines();

for f in filelist:
    #fn = os.path.splitext(os.path.split(f)[1])[0];
    dir = f.split("\\");
    fn=os.path.splitext(dir[len(dir)-1])[0];
    folder = save_folder+"\\"+dir[len(dir)-3]+"\\"+dir[len(dir)-2];
    
    if not os.path.exists(folder):
        os.makedirs(folder);
    
    cmds.file(f, open=True,force=True,type="LuminyModel");
    spAll();
    setMat(fn,folder);
    cmds.file(folder+"\\"+fn+".ma",type="mayaBinary",f=True,ea=True);