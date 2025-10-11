# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os
import threading

def remove_namespace(name):
    if ':' in name:
        return name.split(':')[-1]
    return name
def lastPath(name):
    if '|' in name:
        return name.split('|')[-1]
    return name
    
def copy_animation_by_name(from_root, to_root):
    start_frame = cmds.playbackOptions(query=True, minTime=True)
    end_frame = cmds.playbackOptions(query=True, maxTime=True)
    from_joints = cmds.listRelatives(from_root, allDescendents=True, type='joint', fullPath=True)
    from_joints.append(from_root)
    
    to_joints = cmds.listRelatives(to_root, allDescendents=True, type='joint', fullPath=True)
    to_joints.append(to_root)
    
    to_joints_dict = {lastPath(cmds.ls(jnt, shortNames=True)[0]): jnt for jnt in to_joints}
    
    count = 0
    for from_joint in from_joints:
        from_joint_name = cmds.ls(from_joint, shortNames=True)[0]
        from_joint_name=remove_namespace(from_joint_name)
        
        if from_joint_name in to_joints_dict:
            to_joint = to_joints_dict[from_joint_name]
            anim_curves = cmds.keyframe(from_joint, query=True, name=True)
            count=count+1
            if not anim_curves:
                continue
            
            for anim_curve in anim_curves:
                anim_data = cmds.keyframe(anim_curve, query=True, time=(start_frame, end_frame), valueChange=True, timeChange=True)
                for time, value in zip(anim_data[0::2], anim_data[1::2]):
                    cmds.setKeyframe(to_joint, time=time, value=value, attribute=anim_curve.split('_')[-1])
    
    print(f"Copy {from_root} To {to_root} Count:{count}。")

def ExportFileToFBX(sfile,ofile):
    rootbone='SM_female_01_a3_rig_rebinding:DHIbody:root'
    try:
        cmds.file(sfile, open=True,force=True);
    except Exception as err:
        print(sfile+' Open Exception : '+str(err)); 
    try:
        cmds.select(rootbone,hi=True);
        nsel = cmds.ls(cmds.ls(sl=True), type="joint")

        # 获取时间滑块的开始和结束帧
        start_frame = cmds.playbackOptions(query=True, minTime=True)
        end_frame = cmds.playbackOptions(query=True, maxTime=True)
        
        # 烘焙骨骼动画
        cmds.bakeResults(rootbone, time=(start_frame, end_frame),hi='below',sm=True,dic=True,pok=True,mr=True)
        newroot = '|'+cmds.duplicate(rootbone)[0];
        copy_animation_by_name(rootbone,newroot);
        cmds.select(newroot,hi=True);
    except Exception as err:
        print(sfile+' Scene Exception : '+str(err));
    try:
        cmds.file(ofile,es=True,f=True,type="FBX export");
        return True
    except Exception as err:
        print(sfile+' Export Exception : '+str(err));
        return False

def DoBatchExport():
    files = cmds.fileDialog2(dialogStyle=2, fileMode=4, okCaption="Select Files To Export")
    folder = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption="Select Output Folder")[0]
    errfile = open(os.path.join(folder,'errfile.txt'), "w");
    errCount=0
    for fpath in files:
        fileName=os.path.splitext(os.path.basename(fpath));
        output=os.path.join(folder,fileName[0]+".fbx")
        isExport=ExportFileToFBX(fpath,output)
        if not isExport:
            errCount=errCount+1
            errfile.write(fpath+'\n')
            errfile.flush()
    errfile.close()
    cmds.confirmDialog( title='Wings Tool', message='Export Finish!\nError File:%d'%errCount, button=['OK'], defaultButton='OK', dismissString='No' )

DoBatchExport();