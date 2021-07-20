# -*- coding: utf-8 -*-
import maya.cmds as cmds;

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