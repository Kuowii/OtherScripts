# -*- coding: utf-8 -*-
import maya.cmds as cmds

class MessageBox: 
   def __init__(self, info):
       try:
           cmds.deleteUI("MessageBox");
       except :
           print('close MessageBox');
       self.msg = cmds.window("MessageBox", w=300, h=100,s=False)
       cmds.columnLayout();
       btn = cmds.button(label=info, w=300, h=100,c=self.close);
       cmds.showWindow(self.msg);
   
   def close(self,sender):
     cmds.deleteUI(self.msg);

def getFaceArea(face):
    r = cmds.polyEvaluate(face,ufa=True );
    return r[0]**0.5;
    
def checkTdStart(self):

    global td_control,offset_control,tsize_control;
    tsize=cmds.intField(tsize_control,q=True, v=True);
    td=cmds.floatField(td_control,q=True, v=True);
    offset=cmds.floatField(offset_control,q=True, v=True);
    
    cmds.ConvertSelectionToFaces();
    cmds.ls(sl=True,long=True) or []
    selected = cmds.filterExpand( sm=34 );
    
    if selected is None or len(selected) <=0 :
        MessageBox("未选中对象！");
        return;
    
    r=[]
    for f in selected:
        fa = getFaceArea(f);
        if abs(fa*tsize-td)>offset:
            r.append(f);
    cmds.select(cl=True);
    cmds.select(r);
    MessageBox(" 选中 %d 个面" % len(r))

version = "EVO UV TD Check v1.0";
MainWin=cmds.window(version);
cmds.window( MainWin, edit=True, widthHeight=(400, 150) );
cmds.columnLayout();
cmds.text(version);
cmds.rowColumnLayout( numberOfColumns=6);
cmds.text("  贴图大小  ");
tsize_control=cmds.intField(v=4096);
cmds.text("  默认密度  ");
td_control=cmds.floatField(v=10.0,precision=4);
cmds.text("  误差  ");
offset_control=cmds.floatField(v=1.0,precision=4);
cmds.button(label=" 检  查 ",command=checkTdStart);

cmds.showWindow(MainWin);

