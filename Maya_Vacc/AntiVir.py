# -*- coding: utf-8 -*-
import maya.cmds as cmds;
import Msg ;

class AntiVacc: 
    @staticmethod
    def clearVacc():
        aa=cmds.ls();
        isVir = False;
        for a in aa:
            if "vaccine_gene" in a:
                cmds.delete(a);
                isVir = True;
            if "breed_gene" in a:
                cmds.delete(a);
                isVir = True;
                        
        if isVir:
            Msg.MessageBox("File has vacc script,pls resave file!");
        else:
            print("File OK(Anti Vacc By Wings).");

