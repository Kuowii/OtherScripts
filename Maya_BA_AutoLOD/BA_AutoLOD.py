# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os
import re
from io import open

class baresetfbx:
    def __init__(self):
        print("baresetfbx create.");
        self.errfiles = [];
    def reset(self,f):
        fp = os.path.join(r'F:\Unity_Projects\BaHaArt\Art_ADY\Art',f);
        fnn =os.path.basename(f).split('.');
        fn = fnn[0];
        fext = fnn[1].lower();
              
        cmds.file(fp,i=1,type="FBX");
        
        isGetLOD = False;
        try:
            cmds.select(fn+"_LOD00");
            isGetLOD = True;
        except:
            isGetLOD = False;
            
        if not isGetLOD:
            isGetNode = True;
            try:
                cmds.select(fn);
            except:
                print("{0} can not get {1}".format(f,fn));
                self.errfiles.append(f);
                isGetNode = False;
            
            if not isGetNode:
                all = cmds.ls(s=1);
                l0 = all[0].replace("Shape","");
                l0 = cmds.rename(l0,fn);
                cmds.select(l0);
            else:
                l0 = cmds.ls(sl=1);
        else:
            l0 = cmds.ls(sl=1);
            
        print("LOD0 is " + str(l0));
        src = l0;
        l1 = cmds.duplicate( src );
        isNeedClean = False;
        
        try:
            cmds.polyReduce( l1,ver=1, p=30);
        except:
            isNeedClean = True;
        
        if isNeedClean:
            #cmds.polyClean(l1);
            cmds.select(l1);
            pmcmd=r'expandPolyGroupSelection; polyCleanupArgList 4 { "0","1","0","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","0","0" };'
            rs = mel.eval(pmcmd);
            src = l1;
            
        l2=cmds.duplicate( src );
        l3=cmds.duplicate( src );
        l4=cmds.duplicate( src );
        l0 = cmds.rename(l0,fn+"_LOD00");
        l1 = cmds.rename(l1,fn+"_LOD01");
        l2 = cmds.rename(l2,fn+"_LOD02");
        l3 = cmds.rename(l3,fn+"_LOD03");
        l4 = cmds.rename(l4,fn+"_LOD04");
        
        if not isNeedClean:
            cmds.polyReduce( l1,ver=1, p=30);
        cmds.polyReduce( l2,ver=1, p=50);
        cmds.polyReduce( l3,ver=1, p=70);
        cmds.polyReduce( l4,ver=1, p=95);
        
        if not isGetLOD:
            cmds.group( l0,l1,l2,l3,l4, n=fn);
        
        allMat = cmds.ls(mat=True)
        for mat in allMat:
            SG = cmds.listConnections('%s.outColor' % mat) 
            shapes = cmds.listConnections(SG, type="mesh") 
            if ((shapes == None) or (shapes == "None") or (shapes == "") or (shapes == [])): 
                continue;
            if mat == "lambert1":
                sha = cmds.shadingNode('lambert', asShader=True, name="MI_NEW_TEMP");
                sg = cmds.sets(empty=True, renderable=True, noSurfaceShader=True);
                cmds.connectAttr( sha+".outColor", sg+".surfaceShader", f=True);
                cmds.sets([l0,l1,l2,l3,l4], e=True, forceElement=sg);
                mat="MI_NEW_TEMP";
                
            cmds.rename(mat,"MI_"+fn);
        
        cmds.select(fn);
        ofp = os.path.join(r'F:\Unity_Projects\BaHaArt\Reduce',fn+"."+fext);
        if not os.path.exists(os.path.dirname(ofp)):
            os.makedirs(os.path.dirname(ofp));
        cmds.file(ofp,es=True,f=True,type="FBX export");
        

def main():
    index_file = cmds.fileDialog2(fileFilter="*.txt",caption="选择目录文件",fm=1);
    filelist = None;
    with open(index_file[0], 'r', encoding='utf-8') as f:
        filelist=f.readlines();
    
    r = baresetfbx();
        
    for f in filelist:
        cmds.file(new=1,f=1);
        r.reset(f);
    print(r.errfiles);
        
main();