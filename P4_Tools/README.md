[toc]

# P4_Tools

P4 工具集。

# Environment
- P4V 2022.2
- UE5.1.1

# ChangeListMarkForDelete
主要用来解决在 UE5 开启大世界后，在删除地图的Actor时，会出现只Checkout文件为Edit，但实际上却删除了的情况，所以此时通过这个脚本来讲ChangList中的Edit文件转换为Delete。
> 其原理就是先Revert然后再标记为Delete。
