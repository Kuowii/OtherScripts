import maya.cmds as cmds
import maya.OpenMaya as om
import math

class Bounds2D:
    def __init__(self,min_x,min_y,max_x,max_y):
        self.min_x=min_x
        self.min_y=min_y
        self.max_x=max_x
        self.max_y=max_y
        self.center_x=(min_x+max_x)/2
        self.center_y=(min_y+max_y)/2
    def __str__(self) -> str:
        return f"[{self.min_x},{self.min_y}] [{self.max_x},{self.max_y}]"

    def __sub__(self,other):
        """
        计算两个边界框之间的最小距离
        """
        if self.max_x == other.max_x and self.min_x == other.min_x and self.max_y == other.may_y and self.min_y == other.min_y:
            return -1

        # 计算在两个方向上的距离
        dist_u = 0
        if self.max_x < other.min_x:
            dist_u = other.min_x - self.max_x
        elif other.max_x < self.min_x:
            dist_u = self.min_x - other.max_x

        dist_v = 0
        if self.max_y < other.min_y:
            dist_v = other.min_y - self.max_y
        elif other.max_y < self.min_y:
            dist_v = self.min_y - other.max_y
            
        return math.sqrt(dist_u * dist_u + dist_v * dist_v)


class UVShell:
    def __init__(self,shapeFn,uvSet,ids,us,vs,id):
        self.FnMesh = shapeFn
        self.uvSet=uvSet
        self.ids=ids
        self.uArray=us
        self.vArray=vs
        self.id=id
        self.calcBounds()
    def calcBounds(self):
        min_u = float('inf')
        min_v = float('inf')
        max_u = float('-inf')
        max_v = float('-inf')
        for pid in self.ids:
            u=self.uArray[pid]
            v=self.vArray[pid]
            min_u = min(min_u, u)
            min_v = min(min_v, v)
            max_u = max(max_u, u)
            max_v = max(max_v, v)
        self.Bounds=Bounds2D(min_u,min_v,max_u,max_v)
    def __str__(self) -> str:
        return f"{self.uvSet} shell{self.id} v:{len(self.ids)}"
    def __eq__(self, value: object) -> bool:
        if isinstance(value,UVShell):
            return self.uvSet == value.uvSet and self.FnMesh  == value.FnMesh and self.id==value.id
        return False
        
def getCloestPointsToOther(shell1:UVShell,shell2:UVShell,space = 0.1,texSize = 2048):
    points =[]
    for id in shell1.ids:
        u1,v1 = shell1.uArray[id],shell1.vArray[id]  
        for oid in shell2.ids:
            u2,v2 = shell2.uArray[oid],shell2.vArray[oid]
            dist = math.dist([u1,v1],[u2,v2]) * texSize
            # print(f"{id}[{u1},{v1}] {oid}[{u2},{v2}] {dist} {space}")
            if dist <= space:
                points.append([id,oid])
    return points

def getUVShellList(name):
    selList = om.MSelectionList()
    selList.add(name)
    selListIter = om.MItSelectionList(selList, om.MFn.kMesh)
    pathToShape = om.MDagPath()
    selListIter.getDagPath(pathToShape)
    shapeFn = om.MFnMesh(pathToShape)
    meshNode = pathToShape.fullPathName()
    
    uvSets = cmds.polyUVSet(meshNode, query=True, allUVSets =True)
    allShell = []
    for uvset in uvSets[0:1]:
        
        shells = om.MScriptUtil()
        shells.createFromInt(0)
        nbUvShells = shells.asUintPtr()
 
        uArray = om.MFloatArray()   #array for U coords
        vArray = om.MFloatArray()   #array for V coords
        uvShellIds = om.MIntArray() #The container for the uv shell Ids
 
        shapeFn.getUVs(uArray, vArray)
        shapeFn.getUvShellsIds(uvShellIds, nbUvShells, uvset)
 
        shells = {}
        for i, n in enumerate(uvShellIds):
            if n in shells:
                shells[n].append(i)
            else:
                shells[n] = [i]
        for s in shells.keys():
            allShell.append(UVShell(shapeFn,uvset,shells[s],uArray,vArray,s))
    return allShell
    
def checkUVPadding(mesh,textureSize = 2048,spacePixel = 16):
    errorPoints=[]
    shells = enumerate(getUVShellList(mesh))
    for i,shell1 in  shells:
        for j,shell2 in shells:
            if i==j:continue
            bDist = shell1.Bounds-shell2.Bounds
            #print(f"{mesh}.UVShell[{shell1.id}] {mesh}.UVShell[{shell2.id}] {bDist}")
            if bDist < spacePixel and bDist>=0:
                points=getCloestPointsToOther(shell1,shell2,spacePixel,textureSize)
                for p in points:
                    errorPoints.append(f"{mesh}.map[{p[0]}]")
                    errorPoints.append(f"{mesh}.map[{p[1]}]")
    return errorPoints
        

Preset=[(1024,8),(2048,16)]
config = Preset[1]

class UVPaddingCheckWindow:
    def __init__(self):
        self.window_name = "UVPaddingCheckWindow"
        self.version = "1.0.0"
        self.dp_menu_config = None
        self.text_scroll_list = None
        self.resultDatas=[]
        
    def create_ui(self):
        """创建主UI界面"""
        # 如果窗口已存在，先删除
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        
        # 创建主窗口
        main_window = cmds.window(
            self.window_name,
            title="Wings UVPadding Check " + self.version,
            width=500,
            height=800,
            sizeable=True
        )
        
        # 创建主布局
        main_layout = cmds.columnLayout(
            adjustableColumn=True,
            columnAttach=('both', 5),
            rowSpacing=10
        )
        
        # 第一行: 版本信息Label
        self.create_version_label(main_layout)
        
        # 第二行: 下拉菜单
        self.create_dropdown_menu(main_layout)
        
        # 第三行: 执行按钮
        self.create_action_button(main_layout)
        
        # 分隔线
        cmds.separator(style='in', height=10)
        
        # 第四行开始: 带滑块的列表框
        self.create_scroll_list_with_slider(main_layout)
        
        # 显示窗口
        cmds.showWindow(main_window)
    
    def create_version_label(self, parent_layout):
        """创建版本信息标签"""
        cmds.text(
            label=self.version,
            font="boldLabelFont",
            align="right"
        )
    
    def create_dropdown_menu(self, parent_layout):
        """创建下拉菜单"""
        self.dp_menu_config = cmds.optionMenu(
            label='贴图尺寸',
            changeCommand=self.on_dropdown_change
        )
        global Preset
        for p in Preset:
            cmds.menuItem(label=f"{p[0]}贴图，间隔{p[1]}px")
    
    def create_action_button(self, parent_layout):
        """创建执行按钮"""
        cmds.button(
            label="开始检查",
            command=self.on_execute_command,
            height=40,
            backgroundColor=[0.3, 0.5, 0.8]
        )
    
    def create_scroll_list_with_slider(self, parent_layout):
        """创建带滑块的滚动列表框"""
        cmds.text(label="结果列表:", align="left")
        # 创建滚动列表
        self.resultList = cmds.textScrollList(
            allowMultiSelection=False,
            selectCommand=self.on_list_item_selected,
            height = 500
        )
           
        cmds.setParent('..')  # 返回父布局
    
    # 回调函数区域
    def on_dropdown_change(self, selected_item):
        """下拉菜单改变回调"""
        pass
    
    def on_execute_command(self, *args):
        """执行按钮点击回调"""
        cid = cmds.optionMenu(self.dp_menu_config, query=True, select=True)
        global config,Preset
        config = Preset[cid]
        cmds.textScrollList(self.resultList, edit=True, removeAll=True)
        self.resultDatas=[]
        CheckSelect(self)
    
    def on_list_item_selected(self):
        """列表项选择回调"""
        sid = cmds.textScrollList(
            self.resultList,
            query=True,
            selectIndexedItem=True
        )[0]
        cmds.select(self.resultDatas[sid-1])

    def addResult(self,mesh_node,points):
        self.resultDatas.append(points)
        item=str(mesh_node)+" "+str(len(points))
        cmds.textScrollList(self.resultList, edit=True, append=item)

def CheckSelect(ui:UVPaddingCheckWindow):
    try:
        rsels = cmds.ls(sl=1)
        rsels.extend(cmds.listRelatives())
        sels = cmds.listRelatives(rsels,s=1)
        psels = [cmds.listRelatives(shape, parent=True)[0] for shape in sels if cmds.listRelatives(shape, parent=True)]
    except Exception as err:
        cmds.confirmDialog( title='Wings Tool', message='未选择正确的对象！', button=['OK'], defaultButton='OK', dismissString='No' )
        return
    passed=[]
    unPassed=[]
    for s in psels:
        errorPs = checkUVPadding(s,config[0],config[1])
        if len(errorPs)>0:
            unPassed.append(s)
            ui.addResult(s,errorPs)
        else:
            passed.append(s)
    cmds.confirmDialog( title='Wings Tool', message='检查完成！\n通过：  '+str(len(passed))+"\n未通过："+str(len(unPassed)), button=['OK'], defaultButton='OK', dismissString='No' )
    

def main():
    ui = UVPaddingCheckWindow()
    ui.create_ui()

def onMayaDroppedPythonFile(*args):
    main()
main()