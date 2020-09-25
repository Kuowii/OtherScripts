import maya.cmds as cmds;
from math import pow,sqrt;
version = "GG命名检查 v1.0 by Wings";
raw= None;
high = None;
errorList=[];

def setRaw(*args):
    print "Set Raw.";
    global raw_text,raw;
    selected = cmds.ls(sl=True,long=True) or []
    count = len(selected)
    if count<=0:
        print "raw null select.";
        cmds.text(raw_text,l="未设置",edit=True)
        return;
    elif count==1:
        raw = selected[0];
        print "Set raw ",raw;
        cmds.text(raw_text,l=raw,edit=True)
    else:
        cmds.text(raw_text,l=len+"错误(多个对象)",edit=True)
    return;
    
def setHigh(*args):
    print "Set High.";
    global high_text,high,raw;
    selected = cmds.ls(sl=True,long=True) or []
    count = len(selected)
    if count<=0:
        print "high null select.";
        cmds.text(high_text,l="未设置",edit=True)
        return;
    elif count==1:
        high = selected[0];
        print "Set high ",high;
        cmds.text(high_text,l=high,edit=True);
        Check(raw,high);
    else:
        cmds.text(high_text,l=len+"错误(多个对象)",edit=True)
    return;

def IsInArr(t,arr):
    if(t in arr):
        return True;
    return False;

def MessageBox(info):
    msg = cmds.window()
    cmds.columnLayout()
    cmds.button(label=info, w=300, h=100)
    cmds.showWindow(msg);
    return;

def Check(raw,high):
    if(raw==None or high ==None):
        MessageBox("高模或粗模未设置！");
    else:
        print('check: high={0},raw={1}'.format(high,raw));
        errorListRaw=[];
        errorListHigh=[];
        childrenRaw = cmds.listRelatives(raw,children=True, fullPath=False) or []
        childrenHigh = cmds.listRelatives(high,children=True, fullPath=False) or []
        for child in childrenRaw:
            if(not IsInArr(child,childrenHigh)):
                errorListRaw.append(child);
                
        for child in childrenHigh:
            if(not IsInArr(child,childrenRaw)):
                errorListHigh.append(child);
                
        if(len(errorListRaw)>0 or len(errorListHigh)>0):
            ListError(errorListRaw,errorListHigh);
        else:
            MessageBox("命名完全一致！");
    return;
        
class SelBtn:
    btn=None;
    def create(self,target):
        self.t=target;
        self.btn=cmds.button();
        cmds.button(self.btn,l=target,edit=True,command=lambda x:cmds.select(target,hi=True,add=False));
        
    def setcolor(self,col):
        cmds.button(self.btn,edit=True,bgc=col);

def ListError(errorListRaw,errorListHigh):
    errorWin=cmds.window();
    cmds.window(errorWin,t="Result", edit=True);
    cmds.columnLayout(rs=5);
    max = len(errorListRaw);
    bts=[]
    for index in range(max):
        btn=SelBtn();
        btn.create(errorListRaw[index]);
        bts.append(btn);
        
    max = len(errorListHigh);
    for index in range(max):
        btn=SelBtn();
        btn.create(errorListHigh[index]);
        bts.append(btn);
        btn.setcolor([1,0,0]);
        
    cmds.showWindow(errorWin);
    return;

NameCheckWin=cmds.window(version);
cmds.window( NameCheckWin, edit=True, widthHeight=(300, 100) );
cmds.columnLayout(rs=10);
cmds.text(version);
cmds.rowColumnLayout( numberOfColumns=2,cs=[2,10],rs=[1,10]);

cmds.button(label="设置粗模",command=setRaw);
raw_text=cmds.text();
cmds.text(raw_text,l="未设置",edit=True);

cmds.button(label="设置高模",command=setHigh);
high_text=cmds.text();
cmds.text(high_text,l="未设置",edit=True);

cmds.showWindow(NameCheckWin);