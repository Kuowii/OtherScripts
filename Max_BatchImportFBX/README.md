[toc]

# OtherScripts

## MaxBatchImportFBX

这个脚本的作用是把多个 **FBX动画合并到一个场景**，由于使用 **xaf** 文件进行中间转换，所以会在FBX的路径中生成对应的过程文件。



- 2021-07-20
- Max 2019

### 技术Note

1. 使用DotNet的文件对话框进行选择（多选/单选）
2. 按指定类型选择对象
3. 调整动画轴的长度（获取到对象的最后一帧关键帧所在的时间点）
4. 打开文件和写入文本记录文件


### 更新日志
- 2021_07_22
1. 添加了UI界面。
2. 增加了输出说明文件的功能，可以区分时间轴对应帧对应的动画。
3. 增加了删除中间过程的 **xaf** 文件的功能。

- 2021_07_21
更新了动画末尾的计算方法，现在能正确地获取到组合后的动画长度了。

