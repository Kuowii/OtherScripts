# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os
import threading

class BatchExportWindow:
    def __init__(self):
       try:
           cmds.deleteUI("BatchExportWindow");
       except :
           print('close BatchExportWindow');
           self.version = "Batch Export v1.0";
       self.buildUI();
           
    def buildUI(self):
        self.MainWin=cmds.window(self.version);
        cmds.window( self.MainWin, edit=True, widthHeight=(400, 150) );
        cmds.columnLayout();
        cmds.text(self.version);
        cmds.rowColumnLayout( numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 50), (2, 300),(3, 50)] );
        cmds.text( label='Export Path' )
        self.txt_out = cmds.textField();
        cmds.button(label=" Browser ",command=self.browsrOutput);
        cmds.button(label=" Export ",command=self.startExport);
        cmds.showWindow(self.MainWin);
        
    def startExport(self,sender):
        print("Start Export");
        out = cmds.textField(self.txt_out,tx=1,q=1); 
        sel=[];
        for s in cmds.ls(sl=1):
            sel.append(s);
        for s in sel:
            cmds.select(s);
            fp = os.path.join(out,s+".fbx")
            cmds.file(fp,es=True,f=True,type="FBX export");

    def browsrOutput(self,sender):
        save_folder = cmds.fileDialog2(caption="Select Export Result Folder",fm=3)[0];
        cmds.textField(self.txt_out,tx=save_folder,edit=1);

BatchExportWindow();
