import maya.cmds as cmds

def get_mirror_name(name, prefix_left='L_', prefix_right='R_'):
    return name.replace(prefix_left, prefix_right, 1)

def mirror_animation(axis='YZ'):
    """
    将选中的对象的动画进行左右镜像。

    参数:
    axis (str): 镜像的轴，默认为 'YZ'，表示通过 YZ 平面进行镜像。
    """
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("请先选择要镜像的对象。")
        return

    mirror_axis = {'YZ': [1, -1, -1], 'XZ': [-1, 1, -1], 'XY': [-1, -1, 1]}[axis]

    for obj in selected_objects:
        keyframes = cmds.keyframe(obj, query=True, timeChange=True)
        if not keyframes:
            #cmds.warning(f"对象 {obj} 没有动画。")
            continue
        print(obj)
        mirrored_obj = get_mirror_name(obj,'_l','_r')
        print(mirrored_obj)
        if not cmds.objExists(mirrored_obj):
            cmds.warning(f"镜像对象 {mirrored_obj} 不存在。")
            continue
            
        for time in keyframes:
            translation = cmds.getAttr(f"{obj}.translate", time=time)[0]
            rotation = cmds.getAttr(f"{obj}.rotate", time=time)[0]

            mirrored_translation = [translation[i] * mirror_axis[i] for i in range(3)]
            mirrored_rotation = [rotation[i] * mirror_axis[i] for i in range(3)]
            cmds.setKeyframe(mirrored_obj, time=time, attribute='translateX', value=mirrored_translation[0])
            cmds.setKeyframe(mirrored_obj, time=time, attribute='translateY', value=mirrored_translation[1])
            cmds.setKeyframe(mirrored_obj, time=time, attribute='translateZ', value=mirrored_translation[2])
            cmds.setKeyframe(mirrored_obj, time=time, attribute='rotateX', value=mirrored_rotation[0])
            cmds.setKeyframe(mirrored_obj, time=time, attribute='rotateY', value=mirrored_rotation[1])
            cmds.setKeyframe(mirrored_obj, time=time, attribute='rotateZ', value=mirrored_rotation[2])

    print("动画镜像完成。")

# 示例用法：选择要镜像的对象，然后运行镜像函数
mirror_animation('XY')