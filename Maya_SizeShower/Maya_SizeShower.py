# -*- coding: utf-8 -*-
import maya.cmds as cmds

def get_select_bounds(*args):
    x=0
    y=0
    z=0
    # 获取当前选中的对象
    selected_objects = cmds.ls(selection=True)
    
    if selected_objects:
        obj = selected_objects[0]
        # 获取对象的 Bounding Box 信息 (min 和 max 的坐标值)
        bbox = cmds.exactWorldBoundingBox(obj)   
        # 计算长、宽和高
        x = bbox[3] - bbox[0]
        y = bbox[4] - bbox[1]
        z = bbox[5] - bbox[2]
    return x,y,z

# 定义更新函数，获取选中对象的 Bounds 并更新 UI 面板
def update_bounds_info(*args):
    x,y,z=get_select_bounds();
    cmds.text("xText", edit=True, label=f"X: {x:.2f}")
    cmds.text("yText", edit=True, label=f"Y: {y:.2f}")
    cmds.text("zText", edit=True, label=f"Z: {z:.2f}")
    
def hide_headsUpDisplay(*args):
    try:
        cmds.headsUpDisplay( 'HUDSizeInfo', rem=True )
    except:
        pass
    
def show_headsUpDisplay(*args):
    hide_headsUpDisplay()
    cmds.headsUpDisplay( 'HUDSizeInfo', section=1, block=0, blockSize='medium', label='Size', labelFontSize='large', command=get_select_bounds, event='SelectionChanged', nodeChanges='attributeChange' )
    

# 创建或显示 UI 面板
def create_ui():
    if cmds.window("SizeInfoWindow", exists=True):
        cmds.deleteUI("SizeInfoWindow")
    
    cmds.window("SizeInfoWindow", title="Size Info", widthHeight=(200, 100))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.rowLayout(numberOfColumns=3)
    cmds.text("xText", label="X: N/A")
    cmds.text("yText", label="Y: N/A")
    cmds.text("zText", label="Z: N/A")
    cmds.setParent("..")  # 返回到父布局

    # 第二行包含两个按钮
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Show",command=show_headsUpDisplay)
    cmds.button(label="Hide",command=hide_headsUpDisplay)
    cmds.setParent("..")  # 返回到父布局
    
    cmds.showWindow("SizeInfoWindow")

    # 设置一个事件监听器，当选中对象改变时，触发更新函数
    cmds.scriptJob(event=("SelectionChanged", update_bounds_info), parent="SizeInfoWindow")
    update_bounds_info()

# 运行 UI 面板创建函数
create_ui()

def onMayaDroppedPythonFile(*args):
    create_ui()