# -*- coding: utf-8 -*-
import maya.cmds as cmds;
import maya.mel as mel;
import math;

def vector3Equal(a,b):
    bx = math.fabs(a[0]-b[0]) < 0.0001;
    by = math.fabs(a[1]-b[1]) < 0.0001;
    bz = math.fabs(a[2]-b[2]) < 0.0001;
    return bx and by and bz;

def traCheck(obj,default = [0,0,0]):
    t = cmds.getAttr(obj+'.translate')[0];
    return vector3Equal(t,default);

def rotCheck(obj,default = [0,0,0]):
    t = cmds.getAttr(obj+'.rotate')[0];
    return vector3Equal(t,default);

def scaCheck(obj,default = [1,1,1]):
    t = cmds.getAttr(obj+'.scale')[0];
    return vector3Equal(t,default);

def transformCheck(obj):
    return scaCheck(obj) and traCheck(obj) and rotCheck(obj);

def polyCheck(obj):
    cmd = r'polyCleanupArgList 4 { "0","2","1","0","1","1","1","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };'
    rs = mel.eval(cmd);
    return not len(rs) > 0;

def getFaceTexelDensity(face,ts):
    ufa = cmds.polyEvaluate(face,ufa=True );
    wfa = cmds.polyEvaluate(face,wfa=True );
    return (ts*ufa[0]/wfa[0])**0.5;

def uvTexelDensityCheck(obj,texSize = 1024,default = 6.0):
    cmds.ConvertSelectionToFaces();
    faces = cmds.ls(sl=1);
    ufa = cmds.polyEvaluate(faces,ufa=True );
    wfa = cmds.polyEvaluate(faces,wfa=True );
    t = texSize*ufa[0]/wfa[0]*0.5;
    return t < default;
