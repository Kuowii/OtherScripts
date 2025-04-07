# -*- coding: utf-8 -*-
import maya.cmds as cmds
from maya import OpenMaya as om

def find_non_planar_quads(tolerance = 1e-6):
    selected = cmds.ls(selection=True, long=True)
    if not selected:
        cmds.confirmDialog(message="请选择至少一个对象")
        return

    # 获取所有选中的变换节点（包含mesh的父节点）
    meshes = []
    for obj in selected:
        obj_type = cmds.objectType(obj)
        if obj_type == 'transform':
            # 检查是否有mesh子节点
            shapes = cmds.listRelatives(obj, shapes=True, type='mesh', fullPath=True)
            if shapes:
                meshes.append(obj)
        elif obj_type == 'mesh':
            # 获取父变换节点
            parents = cmds.listRelatives(obj, parent=True, fullPath=True)
            if parents:
                meshes.append(parents[0])

    if not meshes:
        cmds.confirmDialog(message="选中的对象中没有多边形网格")
        return

    non_planar_faces = []
    
    for mesh in meshes:
        # 准备API对象
        sel = om.MSelectionList()
        try:
            sel.add(mesh)
        except:
            continue

        dagPath = om.MDagPath()
        try:
            sel.getDagPath(0, dagPath)
        except:
            continue

        mesh_fn = om.MFnMesh(dagPath)

        # 获取所有顶点坐标（世界空间）
        points = om.MPointArray()
        mesh_fn.getPoints(points, om.MSpace.kWorld)
        vtx_positions = [(points[i].x, points[i].y, points[i].z) for i in range(points.length())]

        # 遍历所有面
        num_faces = mesh_fn.numPolygons()
        for face_idx in range(num_faces):
            # 获取面的顶点索引
            vtx_indices = om.MIntArray()
            mesh_fn.getPolygonVertices(face_idx, vtx_indices)
            if vtx_indices.length() != 4:
                continue  # 仅处理四边面

            # 转换为Python列表
            vtx_list = [vtx_indices[i] for i in range(vtx_indices.length())]

            # 获取四个顶点的坐标
            try:
                A = vtx_positions[vtx_list[0]]
                B = vtx_positions[vtx_list[1]]
                C = vtx_positions[vtx_list[2]]
                D = vtx_positions[vtx_list[3]]
            except IndexError:
                continue  # 忽略无效索引

            # 计算向量AB, AC, AD
            AB = [B[0]-A[0], B[1]-A[1], B[2]-A[2]]
            AC = [C[0]-A[0], C[1]-A[1], C[2]-A[2]]
            AD = [D[0]-A[0], D[1]-A[1], D[2]-A[2]]

            # 计算叉乘 AC × AD
            cross_x = AC[1]*AD[2] - AC[2]*AD[1]
            cross_y = AC[2]*AD[0] - AC[0]*AD[2]
            cross_z = AC[0]*AD[1] - AC[1]*AD[0]

            # 标量三重积（AB · (AC × AD)）
            triple = AB[0]*cross_x + AB[1]*cross_y + AB[2]*cross_z

            if abs(triple) > tolerance:
                face_name = "{}.f[{}]".format(mesh, face_idx)
                non_planar_faces.append(face_name)

    # 选中非平面四边面
    if non_planar_faces:
        cmds.select(non_planar_faces, replace=True)
        #print("发现 {} 个非平面四边形面，已选中。".format(len(non_planar_faces)))
        cmds.confirmDialog(message="发现 {} 个非平面四边形面，已选中。".format(len(non_planar_faces)))
    else:
        cmds.select(clear=True)
        #print("所有四边形面均为平面。")
        cmds.confirmDialog(message='所有四边形面均为平面!')

# find_non_planar_quads(0.01)

class MayaPlanarCheckWindow:
    def __init__(self):
        self.create_ui()
        
    def create_ui(self):
        if cmds.window("MayaPlanarCheckWindow", exists=True):
            cmds.deleteUI("MayaPlanarCheckWindow", window=True)
            
        self.win = cmds.window("MayaPlanarCheckWindow", title="Wings 非平面面检测 1.0", widthHeight=(500, 150))
        main_layout = cmds.columnLayout(adjustableColumn=True)
        # 容差控制区
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(80, 150, 80))
        cmds.text(label="容差值：")
        self.tolerance_slider = cmds.floatSliderGrp('toleranceSlider',
            field=True,
            minValue=0.00001,
            maxValue=0.5,
            value=0.001,
            step=0.0001,
            dragCommand=self.update_tolerance,
            changeCommand=self.update_tolerance)    
        # 操作按钮区
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150))
        cmds.button(label="检测非平面面", command=self.check) 
        cmds.showWindow(self.win)

    def update_tolerance(self,value):
        #print(value)
        pass
        
    def check(self,sender):
        vtolerance = cmds.floatSliderGrp(self.tolerance_slider,query=True, value=True)
        #print(tolerance)
        find_non_planar_quads(vtolerance)
        
def onMayaDroppedPythonFile(*args):
    main()

def main():
    mpcw = MayaPlanarCheckWindow()

main()