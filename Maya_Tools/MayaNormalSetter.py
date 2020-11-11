# 设置顶点法线和面法线一致（软边状态下边缘更锐利）

import maya.cmds as cmds
import re #regular expression

cmds.ConvertSelectionToFaces();
fs = cmds.filterExpand( sm=34 );
for f in fs:
    node = f.split('.')[0];
    pi = cmds.polyInfo(f, fn=True);
    vss = cmds.polyInfo(f,fv = True);
    fn = re.findall(r"[\w.-]+", pi[0]); # convert the string to array with regular expression
    vssre = re.findall(r"[\w]+",vss[0]);
    
    
    vs = [];
    
    for index in range(2,len(vssre)):
        vs.append("{0}.vtx[{1}]".format(node,vssre[index]));
    
    cmds.select(vs,r = True);
    cmds.polyNormalPerVertex( xyz = (float(fn[2]),float(fn[3]),float(fn[4]) ) );