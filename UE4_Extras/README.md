[toc]

# OtherScripts

## VertexAnimationTools

- 2021-07-27
- Max 2021
- UE 4.26.2

这个工具是UE官方提供的一个工具，主要用来处理**骨骼动画转换为顶点动画**。

[UE4官方文档](https://docs.unrealengine.com/4.26/zh-CN/AnimatingObjects/SkeletalMeshAnimation/Tools/VertexAnimationTool/)

默认的路径在：`Engine\Extras\3dsMaxScripts\VertexAnimationTools.ms`

但是由于这个工具会在每帧顶点计算的时候默认会 **重新构造面法线**，会造成一些面法线反向的问题，所以添加了控制选项来选择是否重新构造。

为了便于预览每帧时的状态，可以选择保留不删除Snap的临时网格。

### 一些关键函数说明
- `makeSnapshotsReturnArray` : 把网格在需要的帧进行快照
