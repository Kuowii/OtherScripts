# -*- coding: utf-8 -*-
import maya.cmds as cmds

def clean_missing_plugin_nodes():
    """
    清理错误节点
    """
    unknown_nodes = cmds.ls(type='unknown')
    unknown_dag_nodes = cmds.ls(type='unknownDag')
    all_unknown = set(unknown_nodes + unknown_dag_nodes)
    
    nodes_to_delete = list(all_unknown)
    for node in all_unknown:
        try:
            connections = cmds.listConnections(node, type='shadingEngine') or []
            for sg in connections:
                if sg not in nodes_to_delete and sg != 'initialShadingGroup':
                    nodes_to_delete.append(sg)
        except:
            pass
    deleted_count = 0
    for node in nodes_to_delete:
        try:
            if cmds.objExists(node):
                cmds.lockNode(node, lock=False)
                cmds.delete(node)
                print(f"Clean node {node} success.")
                deleted_count += 1
        except Exception as e:
            print(f"Clean node {node} failed,{str(e)}")
    
    unknown_plugins = cmds.unknownPlugin(q=True, list=True) or []
    up_count=len(unknown_plugins)
    for plugin in unknown_plugins:
        try:
            cmds.unknownPlugin(plugin, remove=True)
            print(f"Clean plugin {plugin}")
        except:
            pass
            
    cmds.confirmDialog( title='Wings Tool', message=f"Clean finish ({deleted_count},{up_count})", button=['OK'], defaultButton='OK')
    if up_count>0 or deleted_count>0:
        cmds.file(modified=True)
        
clean_missing_plugin_nodes()