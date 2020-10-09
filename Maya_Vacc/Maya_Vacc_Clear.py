import maya.cmds as cmds

def MessageBox(info):
    msg = cmds.window()
    cmds.columnLayout()
    cmds.button(label=info, w=300, h=100)
    cmds.showWindow(msg);
    return;

aa=cmds.ls();
isVir = False;
for a in aa:
    if "vaccine_gene" in a:
        cmds.delete(a);
        isVir = True;
    if "breed_gene" in a:
        cmds.delete(a);
        isVir = True;
                
if isVir:
    MessageBox("清除成功");
else:
    MessageBox("未感染");