# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om
import os
import tempfile

# 获取系统临时目录
temp_dir = tempfile.gettempdir()

def pivot_check(src,dst):
    space = 0.01;
    sbox=cmds.exactWorldBoundingBox(src)
    dbox=cmds.exactWorldBoundingBox(dst)
    for i,v in enumerate(sbox):
        factor=abs(v-dbox[i])
        if factor > space:
            return False
    return True
    
def get_files_with_extension(directory, extension):
    matching_files = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(extension):
                name=os.path.splitext(filename)[0]
                full_path = os.path.join(root, filename)
                i=1
                newname=name
                while newname in matching_files:
                    newname=f'{name}_{i}'
                matching_files[newname]=full_path
    return matching_files
    
def create_fbx_reference(fbx_path, reference_name):
    # 创建 FBX 引用
    refName=reference_name+'RN'
    if cmds.objExists(refName):
        file_path = cmds.referenceQuery(refName, filename=True)
        print(f"Reference {reference_name} already exists. Removing it.")
        cmds.file(file_path, removeReference=True)  # 如果已经有该引用，移除
        
    # 创建引用
    fpath = cmds.file(fbx_path, reference=True, namespace=reference_name)
    return fpath
    
def pivot_check_byroot(srcRoot,dstRoot,logPath):
    srcFiles=get_files_with_extension(srcRoot,'fbx')
    dstFiles=get_files_with_extension(dstRoot,'fbx')
    f = open(logPath, 'w')
    for srcKey in srcFiles.keys():
        if srcKey not in dstFiles:
            #print(f'{srcKey} not found matched file.')
            f.write(f'{srcKey}({srcFiles[srcKey]}) not found matched file.\n')
            continue    
        create_fbx_reference(srcFiles[srcKey],"SrcRef")
        create_fbx_reference(dstFiles[srcKey],"DstRef")
        
        src = cmds.referenceQuery('SrcRefRN', nodes=True)[0]
        dst = cmds.referenceQuery('DstRefRN', nodes=True)[0]
        r = pivot_check(src,dst)
        if not r:
            f.write(f'Not Pass {srcFiles[srcKey]}\n')
       
def onMayaDroppedPythonFile(*args):
    main()
    
class PivotCheckWindow:
    def __init__(self):
        self.create_ui()
        
    def create_ui(self):
        if cmds.window("PivotCheckWindow", exists=True):
            cmds.deleteUI("PivotCheckWindow", window=True)
            
        self.SettingsPath=os.path.join(temp_dir, 'PivotCheckSettings.txt');
        self.win = cmds.window("PivotCheckWindow", title="Wings PivotCheck 1.0", widthHeight=(500, 150))
        cmds.columnLayout(adjustableColumn=True)
        self.uPathSrc=cmds.textField()
        self.uPathDst=cmds.textField()
           
        if os.path.exists(self.SettingsPath):
            with open(self.SettingsPath, 'r') as f:
                lines = f.readlines()
                cmds.textField(self.uPathSrc,edit=True, text=lines[0].strip())
                cmds.textField(self.uPathDst, edit=True,text=lines[1].strip())
                
        cmds.button( label='Check', command=self.check)
        cmds.showWindow(self.win)
        
    def check(self,sender):
        srcRoot = cmds.textField(self.uPathSrc,query=True, text=True)
        dstRoot = cmds.textField(self.uPathDst,query=True, text=True)     
        with open(self.SettingsPath, 'w') as f:
            f.write(srcRoot + '\n')
            f.write(dstRoot + '\n')
        
        dstLogPath = os.path.join(dstRoot,"result.txt")
        pivot_check_byroot(srcRoot,dstRoot,dstLogPath)
        
    def check_select(self,sender):
        sels=cmds.ls(sl=1)
        r = pivot_check(sels[0],sels[1])
        if r:
            cmds.confirmDialog(message='检查通过！')
        else:
            cmds.confirmDialog(message='检查未通过！')

def main():
    ppwin = PivotCheckWindow()

main()