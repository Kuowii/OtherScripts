# 1.5 增加对于UV点的检测

import maya.cmds as cmds;
from math import pow,sqrt;
version = "LodCheck v1.5 by Wings";

high=[];
low=[];
vtx_list = [];
high_text=None;
low_text=None;
offset=0;

def test(*args):
    selected = cmds.ls(sl=True,long=True) or []
    print len(selected)," selected"
    for eachSel in selected:
        print eachSel;    
    return;

def Get_UVDistance(a, b):
    return sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))

def GetDistance(a, b):
    if len(a)==3:
        Dis=sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2)+pow(a[2]-b[2],2))       
    if len(a)==2:    
        Dis = sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))
    return Dis
  
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
    global high,high_uv
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
#get highuv       
    high_uv = getUVs()
        
    return;

def setLow(*args):
    print "Set low.";
    global high;
    global low,low_uv
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
#get lowuv        
    low_uv = getUVs()
       
    return;
    
#select UV Vertex
def getUVs(*args):
    global Selection_last 
    cmds.select(cmds.polyListComponentConversion(tuv = True), r = True)
    Selection_last = cmds.ls(sl=True, fl=True)
    cmds.select(clear=True)
    uvlist=[]
    for i in Selection_last:
        uvlist.append( cmds.polyEditUV(i, query = True))
    return uvlist
    
#Check Mesh    
def check_Mesh(*args):    
    global high,low
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
    num2 = range(0, len(Selection_last))        
    for iiii in num2:
        if iiii in num_list:
            cmds.select(vtx_list[iiii],tgl=True)
            outlook += 1
        else:
            continue       
    if outlook == 0:
        cmds.window()
        cmds.columnLayout()
        cmds.button(label="Lod Perfect total:"+str(num+1), w=300, h=100)
        cmds.showWindow()
    else:
        cmds.window()
        cmds.columnLayout()
        cmds.button(label="Lod ex:"+str(outlook), w=300, h=100)
        cmds.showWindow()
    return;
           
#Check  UV    
def check_UV(*args):    
    global high_uv,low_uv,offset
    repeat = []
    num = -1
    num_list = []
    offset_uv = offset   
    print "offset_uv=",offset_uv;
    outlook = 0
    
    for ii in low_uv:
        num += 1
        if ii in high_uv:
            continue
        elif isInOffsetDis(high_uv,ii,offset_uv):
            continue
        else:
            num_list.append(num)
                
    num2 = range(0, len(Selection_last))        
    for iiii in num2:
        if iiii in num_list:
            cmds.select(Selection_last[iiii],tgl=True)
            outlook += 1
        else:
            continue       
    if outlook == 0:
        cmds.window()
        cmds.columnLayout()
        cmds.button(label="Lod UV Perfect total:"+str(num+1), w=300, h=100)
        cmds.showWindow()
    else:
        cmds.window()
        cmds.columnLayout()
        cmds.button(label="Lod UV ex:"+str(outlook), w=300, h=100)
        cmds.showWindow()
    return;



LodCheckWin=cmds.window(version);
cmds.window( LodCheckWin, edit=True, widthHeight=(320, 170) );
cmds.columnLayout();
cmds.text(version);
cmds.rowColumnLayout( numberOfColumns=2);
cmds.text("Offset");
offset_control=cmds.floatField(v=offset,cc=offsetEnter,precision=8);
cmds.floatField(offset_control,query=True,v=True);
cmds.button(label="Set High",command=setHigh);
high_text=cmds.text();
cmds.text(high_text,l="High not set",edit=True);
cmds.separator( height=5, style='out' )
cmds.separator( height=5, style='out' )

cmds.button(label="Set Low",command=setLow);
low_text=cmds.text("Low not set");
cmds.text(low_text,l="Low not set",edit=True);
cmds.separator( height=5, style='out' )
cmds.separator( height=5, style='out' )

cmds.button(label="Check Mesh Lod",command=check_Mesh,h=50,bgc=(0.3, 0.5, 0.4));
cmds.button(label="Check UV Lod",command=check_UV,bgc=(0.3, 0.4, 0.5));

cmds.showWindow(LodCheckWin);