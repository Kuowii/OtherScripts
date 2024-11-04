# -*- coding: utf-8 -*-
import maya.cmds as cmds

def get_bottom_center(obj):
    bbox = cmds.exactWorldBoundingBox(obj)
    min_x, min_y, min_z = bbox[0], bbox[1], bbox[2]
    max_x, max_y, max_z = bbox[3], bbox[4], bbox[5]
    center_x = (max_x+min_x)/2
    center_z = (max_z+min_z)/2
    center_y = (max_y+min_y)/2
    return [
    [min_x,min_y,min_z],
    [center_x,min_y,min_z],
    [max_x,min_y,min_z],
    [min_x,min_y,center_z],
    [center_x,min_y,center_z],
    [max_x,min_y,center_z],
    [min_x,min_y,max_z],
    [center_x,min_y,max_z],
    [max_x,min_y,max_z],
    ]
    return 
    

def update_pivot(idx):
    obj = cmds.ls(selection=True)[0]
    x,y,z=get_bottom_center(obj)[idx]
    print(f"New Pivot[{x},{y},{z}]")
    cmds.xform(obj, piv=[x,y,z],ws=True)
    #cmds.setAttr(f"{obj}.translate", x, -y, z)
    cmds.move(-x, -y, -z, obj, relative=True)
    cmds.makeIdentity(obj, apply=True,t=1 )
    

def onMayaDroppedPythonFile(*args):
    main()
    
class PivotPresetWindow:
    def __init__(self):
        self.create_ui()
        
    def create_ui(self):
        if cmds.window("PivotPresetWindow", exists=True):
            cmds.deleteUI("PivotPresetWindow", window=True)

        self.CheckBoxes=[]
        self.win = cmds.window("PivotPresetWindow", title="Wings PivotPreset 1.0", widthHeight=(150, 150))
        cmds.columnLayout(adjustableColumn=True)
        cmds.text("请设置中心位置：")
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 20), (2, 20), (3, 20)], columnSpacing=[(2, 2), (3, 2)], rowSpacing=[(1, 2), (2, 2)])
        for i in range(9): 
            cb = cmds.checkBox(label='',changeCommand=lambda _, idx=i: self.on_checkbox_selected(idx))
            self.CheckBoxes.append(cb)
        cmds.checkBox(self.CheckBoxes[4], edit=True, value=True)
        cmds.setParent("..")
        cmds.button( label='应用', command=self.apply)
        cmds.showWindow(self.win)
        
    def apply(self,sender):
        print(f"Select {self.sel_id}")
        update_pivot(self.sel_id)
        
    def on_checkbox_selected(self,idx):
        self.sel_id = idx
        for i, cb in enumerate( self.CheckBoxes):
            if i != self.sel_id:
                cmds.checkBox(cb, edit=True, value=False)

def main():
    ppwin = PivotPresetWindow()

main()