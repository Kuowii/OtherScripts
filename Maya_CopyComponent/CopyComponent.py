# -*- coding: utf-8 -*-
import maya.cmds as cmds

def doAction():
    sources=cmds.ls(sl=True);
    for s in sources:
        s_dup=cmds.duplicate(s);
        s_dup = cmds.rename(s_dup,f'{s}_b') 
        arms=[f"{s_dup}.f[55175:102312]", f"{s_dup}.f[102316:102478]", f"{s_dup}.f[104969:104971]", f"{s_dup}.f[125764:125774]" ,f"{s_dup}.f[125780]"]
        cmds.select(arms)
        cmds.delete()
        
        s_dup=cmds.duplicate(s);
        s_dup = cmds.rename(s_dup,f'{s}_l')
        arml=[f"{s_dup}.f[55175:78678]", f"{s_dup}.f[104969:104971]", f"{s_dup}.f[125764:125774]"]
        cmds.select(f"{s_dup}.f[:]")
        cmds.select(arml,d=True)
        cmds.delete()
        
        s_dup=cmds.duplicate(s);
        s_dup = cmds.rename(s_dup,f'{s}_r')
        armr=[f"{s_dup}.f[78679:102312]",f"{s_dup}.f[102316:102478]",f"{s_dup}.f[125780]"]
        cmds.select(f"{s_dup}.f[:]")
        cmds.select(armr,d=True)
        cmds.delete()
          
doAction();