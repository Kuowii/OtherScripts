#-*- coding: utf-8-*-
import maya.cmds as cmds;


def getFiles(rootd):
    fss=[];
    for root,dirs,files in os.walk(rootd):
        for file in files:
            fileName=os.path.splitext(file);
            if  fileName[1]== '.ma' or fileName[1]== '.mb':
                fss.append(os.path.join(root, file));
    return fss;


class obj:
   def __init__(self):
       self.dict={};
   def __del__( self ):
       self.dict={};
       
def vaccClear():
    aa=cmds.ls();
    isVir = False;
    for a in aa:
        if "vaccine_gene" in a:
            cmds.delete(a);
            isVir = True;
        if "breed_gene" in a:
            cmds.delete(a);
            isVir = True;
            
    return isVir;


def BatchCheck(files,atReSave = False):
    result_data=obj();
    result_data.rf=[];
    result_data.pf=[];
    result_data.files = files;
    for f in files:
        print(f);
        try:
            cmds.file(f, open=True,force=True);
        except:
            print(f + " open fail.");
            continue;
        isVir = vaccClear();
        if isVir:
            result_data.rf.append(f);
            if atReSave:
                cmds.file(s=True);
        else:
            result_data.pf.append(f);
    return result_data;


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
       
   def BrowserFolder(self,sender):
       root_folder = cmds.fileDialog2(caption=" Select scan folder ",fm=3)[0];
       cmds.textField(self.ui.ftf,tx=root_folder,edit=True);
       
   def changeAutoCb(self,sender):
       self.isAutoResave = cmds.checkBox(self.ui.acb,query=True,v=True );
       
   def mainCheck(self,sender):
       self.changeAutoCb(self);
       root_folder = cmds.textField(self.ui.ftf,tx=True,query=True);
       files = getFiles(root_folder);
       data = BatchCheck(files,self.isAutoResave);
       ResultWin("Vacc_Result",data);
     
   def winMain(self,WinName):
       self.version = "Vacc Batch Check v1.0";
       self.win =cmds.window(WinName,title=WinName, widthHeight=(500, 200) )
       self.mainlayout = cmds.columnLayout( adjustableColumn=True );
       
       cmds.text(self.version);
              
       self.ui=obj();
       cmds.rowColumnLayout(numberOfColumns = 3,p=self.mainlayout)
       cmds.text("Folder");
       self.ui.ftf = cmds.textField(w=270);
       self.ui.fbtn = cmds.button(label="Browser",c=self.BrowserFolder);
       
       cmds.columnLayout( self.mainlayout );
       self.ui.acb = cmds.checkBox( label='Auto Resave',changeCommand=self.changeAutoCb);
       self.ui.sbtn = cmds.button(label="Check",command=self.mainCheck);
       
class ResultWin: 
   def __init__(self,WinName,data):
       try:
           cmds.deleteUI(WinName);
       except :
           print('close '+WinName);
       self.winMain(WinName,data);
       cmds.showWindow(self.win);
          
   def close(self,sender):
       try:
           cmds.deleteUI(self.win);
       except :
           print('Error on close.');
     
   def winMain(self,WinName,data):
       self.version = "Vacc Batch Check v1.0";
       self.win =cmds.window(WinName,title=WinName, widthHeight=(500, 300) )
       self.mainlayout = cmds.columnLayout( adjustableColumn=True );
       
       cmds.text(self.version);
       cmds.text("  ");
       cmds.text("Check {0} files,Pass: {1} ,Unpass: {2}".format(len(data.files),len(data.pf),len(data.rf)));
       
       cmds.frameLayout(label = "Unpass",cll=True,cl = False,p=self.mainlayout);
       for f in data.rf:
           cmds.text(f);
       cmds.frameLayout(label = "Pass",cll=True,cl = True,p=self.mainlayout);
       for f in data.pf:
           cmds.text(f);
       
MainWin("Vacc_Batch");