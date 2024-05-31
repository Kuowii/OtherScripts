[toc]

# OtherScripts

## MayaBSGenerateOnSkin

这个脚本的作用是允许在蒙皮模式下，在动画Pose的形态中对模型的点位置进行编辑，然后将编辑后的网格点位置还原到BindedPose状态下的模型中。

- 2024_05_22
- Maya 2024

### 技术Note

1. 使用点的加权变换矩阵来进行计算
2. 注意要使用 **maya.api.OpenMaya** 的 OpenMaya 2.0 版本来操作，旧版的 OpenMaya 和文档有很多函数和功能对不上。
3. [Maya2024 OpenMaya 官方文档](https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=MAYA_API_REF_py_ref_annotated_html)


### 更新日志

- 2024_05_22
初次上传。