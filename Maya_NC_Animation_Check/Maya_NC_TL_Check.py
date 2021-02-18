# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from math import *

class obj:
   def __init__(self):
       self.dict={};
   def __del__( self ):
       self.dict={};
       
class transform:
    def __init__(self,node):
        self.node = node;
        self.pos=[cmds.getAttr(node + '.tx'),cmds.getAttr(node + '.ty'),cmds.getAttr(node + '.tz')];
        self.rot=[cmds.getAttr(node + '.rx'),cmds.getAttr(node + '.ry'),cmds.getAttr(node + '.rz')];
        
    def isSame(self,other):
        if(other.__class__ != self.__class__):
            #print("Not same class");
            return False;
        bDis=sqrt(pow(self.pos[0]-other.pos[0],2)+pow(self.pos[1]-other.pos[1],2)+pow(self.pos[2]-other.pos[2],2)) < 0.001;
        bRot= ( abs(self.rot[0]-other.rot[0])+abs(self.rot[1]-other.rot[1])+abs(self.rot[2]-other.rot[2]) ) < 3;
        #print('{} - {} bDis:{},bRot:{}'.format(self.node,other.node,bDis,bRot));
        return bDis and bRot;

# ����ָ����λ�Ĺؼ�֡�Ƿ񳬳��˶�����Χ    
def IsOverAniRange(u,max,maxLen=50):
    res=obj();
    res.aniEnd=cmds.keyframe( u, time=(max+1,max+maxLen), query=True, keyframeCount=True );
    res.aniStart=cmds.keyframe( u, time=(-1,-maxLen), query=True, keyframeCount=True );
    return res;
    
# ����Ƿ��ж����
def CheckLayers():
    res=obj();
    # Ĭ��4����ʾ��
    res.dlayers = cmds.ls(type='displayLayer');
    res.alayers = cmds.ls(type='animLayer');
    res.count = len(res.dlayers) + len(res.alayers);
    return res;

# ����Ƿ��ж���֡
def CheckAniRange(sel):
    maxT = cmds.playbackOptions(query=True, maxTime=True);
    r=[];
    for i in sel:
        res = IsOverAniRange(i.node,maxT);
        if(res.aniEnd+res.aniStart > 0):
            r.append(i);
    return r;
            
# ȷ�����Transform �Ƿ�λ���б���
def TransformIsIn(tn,tarr):
    for tt in tarr:
        if(tt.isSame(tn)):
            return tt;
    return None;

# �Ƚ�����Transform�б��Ƿ���ȫһ�£����ز�һ�µ�����
def TransformListCompare(l1,l2):
    result = [];
    for t1 in l1:
        t2 = TransformIsIn(t1,l2);
        if(t2!=None):
            l2.remove(t2);
        else:
            result.append(t1);
    return result;
    
def GetNodesByType(root,ts,cb=None):                
    cmds.select(root, hierarchy=True);
    sel = cmds.ls(sl=True);
    r=[];
    for node in sel:
        nt=cmds.nodeType(node);
        for tt in ts:
            if nt == tt:
                if cb!=None:node=cb(node);
                r.append(node);
                break;
    return r;

# ��ĩ֡�����غϼ��        
def CheckClip(sel,root):
    print("CheckClip");
    maxT = cmds.playbackOptions(query=True, maxTime=True);
    cmds.currentTime(maxT);
    sel2=GetNodesByType(root,['joint','transform'],lambda node: transform(node));
    return TransformListCompare(sel,sel2);

# ���������غϼ��    
def CheckRef(sel,refpath):
    print("CheckRef");
    try:
        cmds.file( refpath, reference=True ,iv = True,mnc=False,options='v=0');
        rn = cmds.file( refpath, query=True, referenceNode=True);
        print("Get ref node "+ rn);
        sel2 = GetNodesByType(rn,['joint','transform'],lambda node: transform(node));
        return TransformListCompare(sel,sel2);
    except :
        print('Error on create reference');

# ����������
def MainCheck(sender):
    print("MainCheck");
    resdata = obj;
    resdata.layerRes = None;
    resdata.kvOverRes = None;
    resdata.sediff = None;
    resdata.refdiff = None;
    resdata.offRefRes = None;
    
    selections = cmds.ls(sl=1,sn=True);
        
    if sender.setting.isLayerOver : 
        resdata.layerRes = CheckLayers();
        if resdata.layerRes.count > 4:
            print("Find Layer : "+str(resdata.layerRes.count));
        else:
            print("No Over Layer");
                    
    if not sender.setting.isKVOver and not sender.setting.isPoseSE and not sender.setting.isPoseRef:
        print("No bones check,quit.");
        ResultWin("NC_TL Result",resdata);
        return;
        
    if selections == None or len(selections) != 1:
        MessageBox("δѡ�����������ѡ��");
        return;
    
    MessageBox("����У����Ժ�");
    
    root = selections[0]; 
    tn = transform(root);
    print("Set root : "+tn.node);
    minT = cmds.playbackOptions(query=True, minTime=True);
    cmds.currentTime(minT);
    sel=GetNodesByType(tn.node,['joint','transform'],lambda node: transform(node));
    
    if sender.setting.isOffcialRef : 
        resdata.offRefRes = (sender.setting.orefp == cmds.referenceQuery( root, un=True,f=True));
    
    if sender.setting.isKVOver : 
        resdata.kvOverRes = CheckAniRange(sel);
        if len(resdata.kvOverRes) > 0:
            print("Find KeyFrame Over Range.");
        else:
            print("No KeyFrame Over Range.");
    
    if sender.setting.isPoseSE : 
        resdata.sediff = CheckClip(sel,root);    
        
    if sender.setting.isPoseRef : 
        resdata.refdiff = CheckRef(sel,sender.setting.refp);
            
    cmds.select(cl=True);
    MessageBox("�����ϣ�");
    ResultWin("NC_TL Result",resdata); 
    return;
    
             
class MessageBox: 
   def __init__(self, info,title="MessageBox",ww=300,wh=100):
       try:
           cmds.deleteUI(title);
       except :
           print('close MessageBox');
       self.win = cmds.window("MessageBox", widthHeight=(ww, wh),s=False)
       cmds.columnLayout();
       btn = cmds.button(label=info, w=ww, h=wh,c=self.close);
       cmds.showWindow(self.win);
          
   def close(self,sender):
       try:
           cmds.deleteUI(self.win);
       except :
           print('Error on close.');
           
class ResultWin: 
   def __init__(self,WinName,data=None):
       try:
           cmds.deleteUI(WinName);
       except :
           print('close '+WinName);
       self.data=data;
       self.winMain(WinName);
       cmds.showWindow(self.win);
          
   def close(self,sender):
       try:
           cmds.deleteUI(self.win);
       except :
           print('Error on close ' + WinName);
           
   def winMain(self,WinName):
       self.win =cmds.window(WinName,title=WinName, widthHeight=(500, 600) )
       self.mainlayout = cmds.columnLayout( adjustableColumn=True );
       
       if(self.data==None):
           cmds.text("û�����ݣ�");
           return;
           
       cmds.rowColumnLayout(numberOfColumns = 3,p=self.mainlayout);
       cmds.text(l="�㼶��� : ");
       if self.data.layerRes == None:
           cmds.text(l="δ���",bgc=[1,1,0]);
       elif self.data.layerRes.count>4:
           cmds.text(l="δͨ��",bgc=[1,0,0]);
       else :
           cmds.text(l="��ͨ��",bgc=[0,1,0]);
       cmds.text(l="");
           
       cmds.text(l="����֡��� : ");
       if self.data.kvOverRes == None:
           cmds.text(l="δ���",bgc=[1,1,0]);
       elif len(self.data.kvOverRes) > 0:
           cmds.text(l="δͨ��",bgc=[1,0,0]);
       else :
           cmds.text(l="��ͨ��",bgc=[0,1,0]);
       cmds.text(l="");
       
       cmds.text(l="��βPose��� : ");
       if self.data.sediff == None:
           cmds.text(l="δ���",bgc=[1,1,0]);
           cmds.button(label=" ��  �� ",command=self.ShowSEDiff,enable=False);
       elif len(self.data.sediff) > 0:
           cmds.text(l="δͨ��",bgc=[1,0,0]);
           cmds.button(label=" ��  �� ",command=self.ShowSEDiff,enable=True);
       else :
           cmds.text(l="��ͨ��",bgc=[0,1,0]);
           cmds.button(label=" ��  �� ",command=self.ShowSEDiff,enable=False);
       
       cmds.text(l="����Pose��� : ");
       if self.data.refdiff == None:
           cmds.text(l="δ���",bgc=[1,1,0]);
           cmds.button(label=" ��  �� ",command=self.ShowRefDiff,enable=False);
       elif len(self.data.refdiff) > 0:
           cmds.text(l="δͨ��",bgc=[1,0,0]);
           cmds.button(label=" ��  �� ",command=self.ShowRefDiff,enable=True);
       else :
           cmds.text(l="��ͨ��",bgc=[0,1,0]);
           cmds.button(label=" ��  �� ",command=self.ShowRefDiff,enable=False);
       
       cmds.text(l="ָ�����ü�� : ");
       if self.data.offRefRes == None:
           cmds.text(l="δ���",bgc=[1,1,0]);
       elif not self.data.offRefRes:
           cmds.text(l="δͨ��",bgc=[1,0,0]);
       else :
           cmds.text(l="��ͨ��",bgc=[0,1,0]);
       cmds.text(l="");
           
       return;

   def ShowRefDiff(self,sender):
        sel=[];
        for n in self.data.refdiff:
            sel.append(n.node);
        cmds.select(cl=True);
        cmds.select(sel);
        
   def ShowSEDiff(self,sender):
        sel=[];
        for n in self.data.sediff:
            sel.append(n.node);
        cmds.select(cl=True);
        cmds.select(sel);
          
          
class MainWin: 
   def __init__(self,WinName):
       try:
           cmds.deleteUI(WinName);
       except :
           print('close '+WinName);
       self.winMain(WinName);
       cmds.showWindow(self.win);
          
   def close(self,sender):
       try:
           cmds.deleteUI(self.win);
       except :
           print('Error on close.');
       
   def changePoseRefCB(self,sender):
       self.posref.isPoseRef = cmds.checkBox(self.posref.cb,query=True,v=True);
       cmds.textField(self.posref.tf,enable=self.posref.isPoseRef,edit=True);
       cmds.button(self.posref.btn,enable=self.posref.isPoseRef,edit=True);
       
   def SelectRefFile(self,sender):
       filename = cmds.fileDialog2(fileMode=1, caption="Select Base Pose File",fileFilter="Maya Files (*.ma *.mb);;MAll Files (*.*)");
       cmds.textField(self.posref.tf,tx=filename[0],edit=True);
       
   def changeOffRef(self,sender):
       self.batch.cbvofref = cmds.checkBox(self.batch.cbofref,query=True,v=True);
       cmds.textField(self.batch.tfofref,enable=self.batch.cbvofref,edit=True);
       
   def CheckClick(self,sender):
       self.setting=obj();
       self.setting.isPoseRef = cmds.checkBox(self.posref.cb,query=True,v=True);
       self.setting.isPoseSE = cmds.checkBox(self.posSE.cb,query=True,v=True);
       self.setting.isKVOver = cmds.checkBox(self.batch.cbkfov,query=True,v=True);
       self.setting.isLayerOver = cmds.checkBox(self.batch.cblayov,query=True,v=True);
       self.setting.isOffcialRef = cmds.checkBox(self.batch.cbofref,query=True,v=True);
       
       if(self.setting.isPoseRef) :
           self.setting.refp=cmds.textField(self.posref.tf,query=True,text=True);
       if(self.setting.isOffcialRef) :
           self.setting.orefp=cmds.textField(self.batch.tfofref,query=True,text=True);
       
       MainCheck(self);
     
   def winMain(self,WinName):
       self.version = "NC_TL Check v1.0";
       self.win =cmds.window(WinName,title=WinName, widthHeight=(500, 600) )
       self.mainlayout = cmds.columnLayout( adjustableColumn=True );
       
       cmds.text(self.version);
       cmds.text("���ǰ��ȷ���Ѿ�ѡ���˸��ڵ�");
       
       self.posref=obj();
       self.posref.isPoseRef=False;
       self.posref.cb=cmds.checkBox( label='Pose ����',changeCommand=self.changePoseRefCB); 
       cmds.rowColumnLayout(numberOfColumns = 3,p=self.mainlayout)
       cmds.text("��� Pose");
       self.posref.tf = cmds.textField(w=370,enable=False);
       self.posref.btn = cmds.button(label="���",enable=False,c=self.SelectRefFile);
       
       
       self.batch=obj();
       self.batch.cbofref=cmds.checkBox( label='ָ������',changeCommand=self.changeOffRef); 
       cmds.rowColumnLayout(numberOfColumns = 2,p=self.mainlayout)
       cmds.text("ָ������");
       self.batch.tfofref = cmds.textField(w=370,enable=False);
       
       cmds.columnLayout( self.mainlayout );
       self.posSE=obj();
       self.posSE.cb=cmds.checkBox( label='��βPose'); 
       
       
       self.batch.cbkfov=cmds.checkBox( label='����֡���'); 
       self.batch.cblayov=cmds.checkBox( label='�������'); 
       
       cmds.button(label=" ��  �� ",command=self.CheckClick);
       
MainWin('NC_TL Checker');