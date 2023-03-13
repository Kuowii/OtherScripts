import maya.cmds as cmds

uscale=(0.5,0.5)
ut0=(0,0.5)
ut1=(0.5,0.5)
ut2=(0,0)
ut3=(0.5,0)
uts=[ut0,ut1,ut2,ut3]

class MatListOption:
    def __init__(self):
        self.menu=cmds.optionMenu(label='Mat')
    def setList(self,mats):
        cmds.menuItem( label="None")
        for m in mats:
            cmds.menuItem( label=m)

class UVMergeWin:
    def __init__(self):
       try:
           cmds.deleteUI("UVMergeWin");
       except :
           print('close UVMergeWin');
       self.winLayout();
       self.showWindow();
    def winLayout(self):
        
        theNodes = cmds.ls(sl = True, dag = True, s = True)
        shadeEng = cmds.listConnections(theNodes , type = "shadingEngine")
        materials = cmds.ls(cmds.listConnections(shadeEng ), materials = True)
        mats=list(dict.fromkeys(materials))
        
        version = "UVMergeWin v1.0";
        self.win=cmds.window("UVMergeWin");
        cmds.window( self.win, edit=True, widthHeight=(400, 150) );
        cmds.gridLayout( numberOfColumns=2,cwh=(120,30) )
        
        self.opts=[]
        for i in range(4):
            opt = MatListOption();
            opt.setList(mats)
            self.opts.append(opt.menu)
        print(self.opts);
        cmds.rowLayout();
        cmds.button("Merge",command=self.start)
        
    def showWindow(self):
       cmds.showWindow(self.win);
    def start(self,sender):
        for i in range(4):
            m=cmds.optionMenu(self.opts[i],q=1,v=1);
            if not m=='None':
                global uscale,ut0,ut1,ut2,ut3
                cmds.select(m)
                cmds.hyperShade(o='')
                meshes = cmds.ls(sl=1)
                uvv=cmds.polyListComponentConversion(meshes,tuv=1)
                cmds.polyMoveUV(uvv, s=uscale,t=uts[i])
            
def main():
    w = UVMergeWin();
    
def onMayaDroppedPythonFile(obj):
    print("onMayaDroppedPythonFile");
    main();
        
main();