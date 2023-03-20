# -*- coding: utf-8 -*-
from maya import cmds

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def boneClip(bones):
    for b in bones:
        attrn=b+".translate";
        tp=cmds.getAttr(attrn)[0];
        cmds.setAttr(attrn+"X",float(truncate(round(tp[0], 3),3)))
        cmds.setAttr(attrn+"Y",float(truncate(round(tp[1], 3),3)))
        cmds.setAttr(attrn+"Z",float(truncate(round(tp[2], 3),3)))
        
        attrn=b+".jointOrient";
        tp=cmds.getAttr(attrn)[0]
        cmds.setAttr(attrn+"X",0)
        cmds.setAttr(attrn+"Y",0)
        cmds.setAttr(attrn+"Z",0)
        
    cmds.confirmDialog( title='Compelet', message='Bone Translate Clip Finish!')

def boneCheck(bones):
    r=[]
    for b in bones:
        attrn=b+".translate";
        tp=cmds.getAttr(attrn)[0];
        isVaild = True;
        for i in range(3):
            tempStr=str(tp[i])
            dlen=len(tempStr[tempStr.find('.') + 1:])
            if dlen>3 and isVaild:
                isVaild = False
                break;
        if not isVaild:
            r.append(b)
            continue;
            
        attrn=b+".jointOrient";
        tp=cmds.getAttr(attrn)[0];
        for i in range(3):
            if tp[i]!=0 and isVaild:
                isVaild = False
                break;
                
        if not isVaild:
            r.append(b)
    return r;
        
class MainWindow: 
   def __init__(self,data=None):
       WinName="BoneTranslateChecker"
       try:
           cmds.deleteUI(WinName);
       except :
           print('close '+WinName);
       self.data=data;
       self.winMain(WinName);
       cmds.showWindow(self.win);
   def refreshAll(self,sender):
       bones=cmds.ls(type='joint')
       print(bones);
       r=boneCheck(bones);
       cmds.textScrollList(self.list,edit=1,ra=1);
       cmds.textScrollList(self.list,edit=1,append=r);
       
   def refreshSel(self,sender):
       bones=cmds.ls(sl=1,type='joint')
       r=boneCheck(bones);
       cmds.textScrollList(self.list,edit=1,ra=1);
       cmds.textScrollList(self.list,edit=1,append=r);
       
   def onSelectResult(self):
       sel = cmds.textScrollList(self.list,query=1,si=1);
       cmds.select(sel)

   def clipSelected(self,sender):
       sel = cmds.textScrollList(self.list,query=1,si=1);
       cmds.select(sel,add=1)
       bones=cmds.ls(sl=1)
       boneClip(bones)
       
   def winMain(self,WinName):
       self.win =cmds.window(WinName,title="Bone Translate Checker By Wings")
       self.rootLayout=cmds.columnLayout()
       cmds.rowColumnLayout(p=self.rootLayout,numberOfRows=1,cs=(50,50))
       cmds.button(l="Refresh All",c=self.refreshAll)
       cmds.button(l="Refresh Select",c=self.refreshSel)
       cmds.button(l="Clip Selected",c=self.clipSelected)
       cmds.paneLayout(p=self.rootLayout)
       self.list=cmds.textScrollList(ams=1,sc=self.onSelectResult);
       
def main():
    win=MainWindow([]);
    
def onMayaDroppedPythonFile(obj):
    main();
    
main()