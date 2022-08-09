[toc]

# OtherScripts

## BA_AutoLOD

这个脚本能够针对指定的节点，使用Maya自带的减面命令，生成LOD组。


### Environment
- Maya2022.2

### 技术Note
在使用减面命令前，要确保当前的模型（Mesh）是一个 [双流形多边形几何体](https://download.autodesk.com/global/docs/maya2014/zh_cn/index.html?url=files/Polygons_overview_Twomanifold_vs._nonmanifold_polygonal_geometry.htm,topicNumber=d30e150949) ，如果不是的话，脚本会执行清理命令，使当前模型转换为双流形几何体后再进行减面。

> 关于双流形几何体，参考Maya官方的解释已经很明显了，双流形几何体可以沿着各种边切割展开（有点展UV的意思），并且最后展成的平面法线是一致的。


### 更新日志
- 2022_08_09
初次上传。