# -*- coding: utf-8 -*-
import maya.cmds as cmds

def scale_anim_curves(value):
    """
    获取当前选中的所有动画曲线，并对每条曲线执行缩放操作。
    """
    # 获取选中的动画曲线节点
    sel = cmds.keyframe(query=True, name=True)
    if not sel:
        cmds.warning("未选中任何动画曲线节点，请选中动画曲线后再运行。")
        return
            
    # 开始撤销块
    cmds.undoInfo(openChunk=True, chunkName='Scale Anim Curves')
    try:
        for c in sel:
            center_pivot = 0
            # 缩放关键帧的值
            # 1. 获取该属性所有关键帧的值
            key_values = cmds.keyframe(c, query=True, valueChange=True)
            
            # 2. 计算波峰（最大值）和波谷（最小值）
            if key_values:
                max_val = max(key_values)
                min_val = min(key_values)
                # 3. 计算中心点（valuePivot）
                center_pivot = (max_val + min_val) * 0.5
                
            cmds.scaleKey(c, valueScale=value,vp=center_pivot)
        cmds.confirmDialog(title='完成', message='缩放操作完成。', button='确定')
    except Exception as e:
        cmds.error("缩放操作失败: {}".format(str(e)))
    finally:
        cmds.undoInfo(closeChunk=True)
        
class KeysModer:
    def __init__(self):
        self.window_name = "WingsKeysModer"
        
    def show_ui(self):
        """显示UI窗口"""
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
            
        self.win = cmds.window(self.window_name, title="Wings 动画曲线缩放工具 v1.0", width=400, height=200)
        
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        
        # 选项部分
        cmds.frameLayout(label="选项", collapsable=True)
        self.scale_value_slider=cmds.floatSliderGrp("scale_value_slider",label="缩放",field=True,minValue=0.00,maxValue=300.00,value=50.00)
        cmds.setParent('..')
        
        # 按钮部分
        cmds.button(label="操作", command=self.do)
        cmds.setParent('..')
       
        cmds.showWindow(self.win)
    def do(self,sender):
        scale_value = cmds.floatSliderGrp(self.scale_value_slider,query=True,value=True)
        scale_value = scale_value/100.00
        scale_anim_curves(scale_value)

if __name__ == "__main__":
    tool = KeysModer()
    tool.show_ui()