# -*- coding: utf-8 -*-
# Made in Maya2024.2 By Wings
from maya import cmds
#import maya.OpenMaya as om
import maya.api.OpenMaya as om

def get_vertex_weights(mesh, indices,skin_cluster=None,joints=None):
    if skin_cluster==None:skin_cluster = cmds.ls(cmds.listHistory(mesh), type='skinCluster')[0]
    if joints==None:joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
    vdata={}
    for v in indices:
        try:
            weights = cmds.skinPercent(skin_cluster, '{}.vtx[{}]'.format(mesh, v), query=True, value=True)
            joint_weights = {joints[i]: weights[i] for i in range(len(joints)) if weights[i] > 0.0}
            vdata[v]=joint_weights
        except Exception as err:
            print(f"Error on {mesh}[{v}] {err}")
    return vdata
    
def get_joint_matrix(joint_name):
    if cmds.objExists(joint_name) and cmds.nodeType(joint_name) == 'joint':
        matrix = cmds.xform(joint_name, query=True, matrix=True, worldSpace=True)
        return matrix
    else:
        raise ValueError(f" {joint_name} not a vaild joint.")
        return None
        
def get_vertex_world_position(mesh, vertex_index):
    vertex_position = cmds.xform(f'{mesh}.vtx[{vertex_index}]', query=True, translation=True, worldSpace=True)
    v_wpos = om.MPoint(vertex_position[0], vertex_position[1], vertex_position[2])
    return v_wpos
        
def weighted_matrix_sum(matxs,weights):
    result_matrix = om.MMatrix()
    for i in range(len(matxs)):
        joint_mat=matxs[i]
        weight=weights[i]
        tmatrix = om.MMatrix(joint_mat)
        weighted_matrix = tmatrix * weight
        result_matrix += weighted_matrix
    return result_matrix

def main():
    base_mesh = cmds.ls(sl=1)[0]
    target_mesh = cmds.ls(sl=1)[1]
    vertex_count = cmds.polyEvaluate(base_mesh, vertex=True)
    skin_cluster = cmds.ls(cmds.listHistory(base_mesh), type='skinCluster')[0]
    joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
    joints_matx = {joints[i]: get_joint_matrix(joints[i]) for i in range(len(joints))}
    weights = get_vertex_weights(base_mesh, list(range(0, vertex_count)),skin_cluster,joints)
    for v,k in weights.items():
        matxs = []
        weights = []
        for wjoint, weight in k.items():
            #print(f"{target_mesh}[{v}] Joint: {wjoint}, Weight: {weight}")
            matxs.append(joints_matx[wjoint])
            weights.append(weight)
        vertex_matx_ltw=weighted_matrix_sum(matxs,weights)
        vertex_matx_wtl=vertex_matx_ltw.inverse()
        v_wpos=get_vertex_world_position(target_mesh,v)
        v_skin_pos=v_wpos * vertex_matx_wtl
        v_bs_pos=v_skin_pos*vertex_matx_ltw
        cmds.xform(f"{base_mesh}.vtx[{v}]", translation=(v_bs_pos[0],v_bs_pos[1],v_bs_pos[2]), worldSpace=True)
    #blend_shape_node = cmds.blendShape(target_mesh,base_mesh, name='blendShapeNode')[0]
    #cmds.setAttr(f'{blend_shape_node}.{target_mesh}', 0.5)
main()