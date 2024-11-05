# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om

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
    
def get_all_mesh_children(parent_node):
    children = cmds.listRelatives(parent_node, children=True, fullPath=True)
    mesh_children = []
    if children:
        for child in children:
            if cmds.nodeType(child) == 'mesh':
                mesh_children.append(child)
            elif cmds.nodeType(child) == 'transform':
                mesh_children.extend(get_all_mesh_children(child))
    return mesh_children
    
def find_nearest_point_on_mesh(obj,sp,ep):
    meshes = get_all_mesh_children(obj)
    start_point = om.MFloatPoint(sp[0], sp[1], sp[2])
    end_point = om.MFloatPoint(ep[0], ep[1], ep[2])
    min_distance = float('inf')
    nearest_point = sp
    direction = end_point-start_point
    
    omlist = om.MSelectionList()
    for mesh in meshes:
        omlist.add(mesh)
        dag_path = omlist.getDagPath(0)
        fn_mesh = om.MFnMesh(dag_path)
        hit_result = fn_mesh.closestIntersection(
        start_point, direction,
        om.MSpace.kWorld, 9999, False)
        omlist.clear()
        if hit_result:
            hit_point = hit_result[0]
            hit_distance = hit_result[1]
            if hit_distance < min_distance:
                nearest_point = [hit_point[0],hit_point[1],hit_point[2]]
    return nearest_point 
    

def update_pivot(idx,isAttach=False):
    obj = cmds.ls(selection=True)[0]
    points = get_bottom_center(obj)
    sp=points[idx]
    if isAttach:
        sp = find_nearest_point_on_mesh(obj,sp,points[4])
    x,y,z=sp
    cmds.xform(obj, piv=[x,y,z],ws=True)
    cmds.move(-x, -y, -z, obj, relative=True)
    cmds.makeIdentity(obj, apply=True,t=1 )
    cmds.delete(obj, ch=True)

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
        self.sel_id = 4
        cmds.setParent("..")
        self.cbAttachMesh = cmds.checkBox(label='吸附到模型')
        cmds.button( label='应用', command=self.apply)
        cmds.showWindow(self.win)
        
    def apply(self,sender):
        isAttach = cmds.checkBox(self.cbAttachMesh,query=True,value=True)
        update_pivot(self.sel_id,isAttach)
        
    def on_checkbox_selected(self,idx):
        self.sel_id = idx
        for i, cb in enumerate( self.CheckBoxes):
            if i != self.sel_id:
                cmds.checkBox(cb, edit=True, value=False)

def main():
    ppwin = PivotPresetWindow()

main()