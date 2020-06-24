import maya.cmds as cmds;
from math import pow,sqrt;
version = "LodCheck v1.1 by Wings";

high=[];
low=[];
vtx_list = [];
high_text=None;
low_text=None;
offset=-1.0;

def test(*args):
    selected = cmds.ls(sl=True,long=True) or []
    print len(selected)," selected"
    for eachSel in selected:
        print eachSel;
    
    return;


def GetDistance(a, b):
  return sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2)+pow(a[2]-b[2],2))
  
def isInOffsetDis(arr,p,off):
    for i in arr:
        if GetDistance(i,p)<=off:
            return True;
    return False;
    

def offsetEnter(self,*args):
    global offset;
    offset=self;
    return;
    
def setHigh(*args):
    print "Set high.";
    global high;
    global high_text;
    high=[];
    selected = cmds.ls(sl=True,long=True) or []
    count = len(selected)  
    if count<=0:
        print "null select.";
        cmds.text(high_text,l="High not set",edit=True)
        return;
    elif count==1:
        print "Set high ",selected[0];
        cmds.text(high_text,l=selected[0],edit=True)
    else:
        cmds.text(high_text,l=len+" selected.",edit=True)
        
    cmds.ConvertSelectionToVertices()
    for i in cmds.filterExpand( sm=31 ):
        high.append(cmds.xform(i,ws=True,q=True,t=True))
    t=cmds.distanceDimension( sp=high[0], high[3] );
    print t
    return;

def setLow(*args):
    print "Set low.";
    global high;
    global low;
    global vtx_list;
    global low_text;
    low=[];
    vtx_list=[];
    selected = cmds.ls(sl=True,long=True) or []
    count = len(selected)  
    if count<=0:
        print "null select.";
        cmds.text(low_text,l="Low not set",edit=True)
        return;
    elif count==1:
        print "Set low ",selected[0];
        cmds.text(low_text,l=selected[0],edit=True)
    else:
        cmds.text(low_text,l=len+" selected.",edit=True)
    
    cmds.ConvertSelectionToVertices()
    for i in cmds.filterExpand( sm=31 ):
        low.append(cmds.xform(i,ws=True,q=True,t=True))
        vtx_list.append(i)
    check(high,low);
    return;
    
def check(high,low):
    repeat = []
    num = -1
    num_list = []
    global vtx_list
    global offset
    print "offset=",offset;
    outlook = 0
    for ii in low:
        num += 1
        if ii in high:
            continue
        elif offset>0 and isInOffsetDis(high,ii,offset):
            continue;
        else:
            repeat.append(ii)
            num_list.append(num)
    
    num2 = range(0, len(vtx_list))
    for iiii in num2:
        if iiii in num_list:
            outlook += 1
            continue
        else:
            cmds.select(vtx_list[iiii], tgl=True)
    if outlook == 0:
        cmds.window()
        cmds.columnLayout()
        cmds.button(label="Lod Perfect total:"+str(num), w=300, h=100)
        cmds.showWindow()
    else:
        cmds.window()
        cmds.columnLayout()
        cmds.button(label="Lod ex:"+str(outlook), w=300, h=100)
        cmds.showWindow()
    return;

LodCheckWin=cmds.window(version);
cmds.window( LodCheckWin, edit=True, widthHeight=(300, 100) );
cmds.columnLayout();
cmds.text(version);
cmds.rowColumnLayout( numberOfColumns=2);
cmds.text("Offset");
offset_control=cmds.floatField(v=offset,cc=offsetEnter);
cmds.floatField(offset_control,query=True,v=True);
cmds.button(label="Set High",command=setHigh);
high_text=cmds.text();
cmds.text(high_text,l="High not set",edit=True);
cmds.button(label="Set Low",command=setLow);
low_text=cmds.text("Low not set");
cmds.text(low_text,l="Low not set",edit=True);

cmds.showWindow(LodCheckWin);