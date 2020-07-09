import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm
import sys
import os

version = "Check Panel v1.0 ";

reload(sys)
sys.setdefaultencoding('utf-8')

# �����������
def utf_8String(StringT):
    utf_8String = StringT
    utf_8String.encode('utf-8')
    utf_8String = unicode(utf_8String, "utf-8")
    return utf_8String


import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm

version = "Check Panel v1.0 ";


# ��鵱ǰ��λ�Ƿ�ΪCM��Meter
def UnitCheck(*args):
    unit = cmds.currentUnit(query=True, linear=True)
    if unit == "cm":
        unitwin = "��ǰ��λ��CM"
    elif unit == "m":
        unitwin = "��ǰ��λ��Meter"
    else:
        unitwin = "��ǰ��λ����CM��Meter"
    return unitwin


# ���ģ��������
limset = 0
def FaceNum_Check(*args):
    global selection
    global limset;
    global fc;
    facecount = cmds.polyEvaluate(selection, t=True)
    limset =int( cmds.textFieldGrp(fc, query=True, tx=True));
    print limset;
    if facecount > limset:
        fcwin = "ģ��������������"
    else:
        fcwin = "��������"
    return fcwin

#��鲢�Ա���ͼ�ߴ�  
def Tex_Check(*args):
    global setlist_out,namelist,display11
    order=-1
    wintext_list=[]
    for i in getTex():
        order +=1      
        if i in setlist_out:
            continue
        else: 
            wintext = namelist[order] +'    '+ getTex()[order]
            display11 = 1             
            wintext_list.append(wintext)         
    return wintext_list
#���������ͼ���ֺͳߴ�
def getTex(*args):
    global namelist
    size=[]
    texlist=[]
    namelist=[]
    allFileNodes = cmds.ls(et="file")
    for i in allFileNodes:
        path = cmds.getAttr(i+'.fileTextureName')
        name = os.path.basename(path)
        size = cmds.getAttr(i+'.outSize')[0]
        size_list=list(size)       
        w=int(size_list[0])
        h=int(size_list[1])
        size_out = str(w) +'*'+ str(h)
        #print size_out
        namelist.append(name)
        texlist.append(size_out)
    return texlist
#���size
def get_texsize(*args): 
    global size_field
    global sco,setlist,setlist_out
    setlist=[]
    setlist_out=[]
    setsize = cmds.textFieldGrp(size_field,query=True, text=True) 
    setlist.append(str(setsize))  
    cmds.textScrollList( sco,append=setlist,h=60,edit=True )
    setlist=cmds.textScrollList( sco, query=True, ai=True)  
    for i in setlist:
        setlist_out.append(i.encode('utf8'))  
#�Ƴ�size           
def del_texsize(*args):
    global sco,setlist ,setlist_out
    setlist_out=[]   
    dell=cmds.textScrollList( sco, query=True, si=True) 
    cmds.textScrollList( sco,edit=True,ri=dell,h=60 ) 
    setlist=cmds.textScrollList( sco, query=True, ai=True)
    for i in setlist:
        setlist_out.append(i.encode('utf8'))     

# ����������
def AxisCheck(*args):
    global selection
    global display1
    NameList_Axis = []
    for i in selection:
        Name = i
        print i
        word = cmds.xform(Name, q=1, ws=1, rp=1)
        if word[0] + word[1] + word[2] != 0:
            NameList_Axis.append(Name.encode('utf8'))
            display1 = 1
        else:
            continue
    return NameList_Axis


# ��鶳��任
def TransformCheck(*args):
    global selection
    global display2
    NameList_Ts = []
    for i in selection:
        Name = i
        moves = cmds.xform(Name, q=1, ws=1, rp=1)
        rotates = cmds.xform(Name, q=1, ws=1, ro=1)
        scales = cmds.xform(Name, q=1, ws=1, s=1)
        if moves[0] + moves[1] + moves[2] != 0:
            NameList_Ts.append(Name.encode('utf8'))
            display2 = 1
        elif rotates[0] + rotates[1] + rotates[2] != 0:
            NameList_Ts.append(Name.encode('utf8'))
            display2 = 1
        elif scales[0] + scales[1] + scales[2] != 3:
            NameList_Ts.append(Name.encode('utf8'))
            display2 = 1
        else:
            continue
    return NameList_Ts


# �������
def OverSides(*args):
    global selection
    global display3, osface
    cmds.select(selection)
    NameList_Os = []
    cmd = r'polyCleanupArgList 4 {"0","2","0","0","1","0","0","0","0","1e-05","0","1e-05","0","0","0","-1","0","0" }'
    result = mm.eval(cmd)
    osface = cmds.ls(sl=True)
    cmds.ConvertSelectionToShell()
    NameList = cmds.ls(sl=True)
    cmds.select(clear=1)
    cmds.hilite(replace=True)
    print osface
    for i in NameList:
        NameList_Os.append(i.split('.')[0].encode('utf8'))
    if len(NameList_Os) != 0:
        display3 = 1
    return NameList_Os


# ���Ť����
def WrapFace(*args):
    global selection
    global display4, wpface
    cmds.select(selection)
    NameList_Wf = []
    cmd = r'polyCleanupArgList 4 {  "0","2","0","0","0","0","0","1","0","1e-05","0","1e-05","0","0","0","-1","0","0" };'
    result = mm.eval(cmd)
    wpface = cmds.ls(sl=True)
    cmds.ConvertSelectionToShell()
    NameList = cmds.ls(sl=True)
    cmds.select(clear=1)
    cmds.hilite(replace=True)
    print wpface
    for i in NameList:
        NameList_Wf.append(i.split('.')[0].encode('utf8'))
    if len(NameList_Wf) != 0:
        display4 = 1
    return NameList_Wf


# ���ģ�Ϳ��ű�
def OpenEdge(*args):
    global selection
    global display5
    global opedge
    NameList_Oe = []
    cmds.select(selection)
    # ѡ��Լ�����ű�
    pm.polySelectConstraint(where=1, type=0x8000, mode=3)
    opedge = cmds.ls(sl=True)
    print opedge
    cmds.ConvertSelectionToShell()
    NameList = cmds.ls(sl=True)
    # ����Լ��
    cmd = r'resetPolySelectConstraint'
    result = mm.eval(cmd)
    cmds.select(clear=1)
    cmds.hilite(replace=True)
    for i in NameList:
        NameList_Oe.append(i.split('.')[0].encode('utf8'))
    if len(NameList_Oe) != 0:
        display5 = 1
    return NameList_Oe


# ѡ������Ӳ��
def Hardedge_Check(*args):
    obj = cmds.ls(selection=True)  # �洢��ǰѡ������
    cmds.polySelectConstraint(m=3, t=0x8000, sm=1)  # ֻѡ��Ӳ��
    sel = cmds.ls(selection=True)  # �洢ѡ���
    cmds.polySelectConstraint(sm=0)  # ��ԭѡzhi��Լ��
    cmds.select(obj)  # ��ԭ֮ǰѡ�������
    cmds.selectMode(component=True)  # ����ѡ��ģʽ
    cmds.selectType(edge=True)  # ����ѡ����Ϊ����ģʽ
    cmds.select(sel)  # ѡ��洢�ı�


# ���UV��ʧ
def UvLose(*args):
    global display7
    global selection, ulface
    cmds.select(selection)
    NameList_Uvlose = []
    cmd = r'polyCleanupArgList 4 { "0","2","0","0","0","0","0","0","0","1e-05","0","1e-05","1","0","0","-1","0","0"  };'
    result = mm.eval(cmd)
    ulface = cmds.ls(sl=True)
    cmds.ConvertSelectionToShell()
    NameList = cmds.ls(sl=True)
    cmds.select(clear=1)
    cmds.hilite(replace=True)
    print ulface
    for i in NameList:
        NameList_Uvlose.append(i.split('.')[0].encode('utf8'))
    if len(NameList_Uvlose) != 0:
        display7 = 1
    return NameList_Uvlose


# ���UV�ص�(Py)
def UVoverlap(*args):
    global selection
    global display8, UVolface
    cmds.select(selection)
    NameList_Uvoverlap = []
    cmds.ConvertSelectionToFaces()
    UVolface = cmds.polyUVOverlap(oc=True)
    cmds.select(UVolface)
    cmds.ConvertSelectionToShell()
    NameList = cmds.ls(sl=True)
    cmds.select(clear=1)
    cmds.hilite(replace=True)
    print UVolface
    for i in NameList:
        NameList_Uvoverlap.append(i.split('.')[0].encode('utf8'))
    if len(NameList_Uvoverlap) != 0:
        display8 = 1
    return NameList_Uvoverlap


# ���UV�Ƿ񳬳���һ����
def UVout_Check(*args):
    global display9, out
    mesh_shape_list = pm.ls(typ='mesh')
    NameList = []
    out = []
    # �ж�UV�Ƿ��ڵ�һ����
    for shape in mesh_shape_list:
        for i in zip(shape.getUVs()[1], shape.getUVs()[0]):
            if i[0] <= 0 or i[0] >= 1:
                NameList.append(shape)
            elif i[1] <= 0 or i[1] >= 1:
                NameList.append(shape)
            else:
                continue
                # ȡ��UV���ڵ�һ���޵�����
    for ii in mesh_shape_list:
        if ii in NameList:
            out.append(str(ii)[:-5])
            cmds.select(str(ii), tgl=1)
        else:
            continue
    cmds.select(clear=1)
    if len(out) != 0:
        display9 = 1
    return out


# ����GetRot����
def GetRot(time):
    global sel
    info = []
    t = cmds.currentTime(time)
    for i in sel:
        # print type(i)
        rotx = cmds.getAttr(i + '.rx')
        roty = cmds.getAttr(i + ".ry")
        rotz = cmds.getAttr(i + ".rz")
        iposInfo = [i, rotx, roty, rotz]
        info.append(iposInfo)
    return info


def GetTran(time):
    info = []
    t = cmds.currentTime(time)
    for i in sel:
        # print type(i)
        tranx = cmds.getAttr(i + '.tx')
        trany = cmds.getAttr(i + ".ty")
        tranz = cmds.getAttr(i + ".tz")
        iposInfo = [i, tranx, trany, tranz]
        info.append(iposInfo)
    print info
    return info


# �Ƚ���β֡��������ת��λ��
def AnKey_Check(*args):
    global selection, sel
    global display10
    display10 = 0
    cmds.select(selection, hierarchy=True)
    sel = cmds.ls(sl=True)
    cmds.select(clear=1)
    print sel
    maxT = cmds.playbackOptions(query=True, maxTime=True)
    minT = cmds.playbackOptions(query=True, minTime=True)
    maxlist_R = GetRot(maxT)
    minlist_R = GetRot(minT)
    maxlist_T = GetTran(maxT)
    minlist_T = GetTran(minT)
    rot = tran = 0
    for i in maxlist_R:
        if i in minlist_R:
            continue
        else:
            rot = 1
    for i in maxlist_T:
        if i in minlist_T:
            continue
        else:
            tran = 1
    if rot + tran == 0:
        wintext = ' '
    else:
        wintext = '��β֡����λ�û���ת��һ��'
        display10 = 1
    return wintext


# ��ѯcheckBox�Ƿ�ѡ���������Num
def checkBoxs(*args):
    # print 'checkBoxs'
    global Num1, Num2, Num3, Num4, Num5, Num6, Num7, Num8, Num9, Num10, Num11, Num12,Num13
    Num1 = cmds.checkBox('checkBox_Unit', q=True, v=True)
    Num2 = cmds.checkBox('checkBox_Fc', q=True, v=True)
    Num3 = cmds.checkBox('checkBox_Ax', q=True, v=True)
    Num4 = cmds.checkBox('checkBox_Ts', q=True, v=True)
    Num5 = cmds.checkBox('checkBox_Os', q=True, v=True)
    Num6 = cmds.checkBox('checkBox_Wf', q=True, v=True)
    Num7 = cmds.checkBox('checkBox_Oe', q=True, v=True)
    # Num8 = cmds.checkBox('checkBox_He', q=True, v=True)
    Num9 = cmds.checkBox('checkBox_UVlose', q=True, v=True)
    Num10 = cmds.checkBox('checkBox_UVoverlap', q=True, v=True)
    Num11 = cmds.checkBox('checkBox_UVOutside', q=True, v=True)
    Num12 = cmds.checkBox('checkBox_Key', q=True, v=True)
    Num13 = cmds.checkBox('checkBox_Texsize', q=True, v=True)
    
    print Num8


# ��������
def CheckReseult(*args):
    global display1, display2, display3, display4, display5, display7, display8, display9, display10
    global wintext_list
    if UnitCheck != None and Num1 == 1:
        cmds.text('��λ���', bgc=(0.5, 0.4, 0.3), h=30)
        cmds.text(UnitCheck());
    if FaceNum_Check != None and Num2 == 1:
        cmds.text('�������', bgc=(0.5, 0.4, 0.3), h=30)
        cmds.text(FaceNum_Check());
    if display1 != 0 and Num3 == 1:
        cmds.text('���������', bgc=(0.3, 0.4, 0.5), h=30)
        for ii in AxisCheck():
            cmds.text(ii + ' ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_Axis)
    if display2 != 0 and Num4 == 1:
        cmds.text('����任', bgc=(0.3, 0.4, 0.5), h=30)
        for ii in TransformCheck():
            cmds.text(ii + '  ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_Tran)
    if display3 != 0 and Num5 == 1:
        cmds.text('�����', bgc=(0.3, 0.4, 0.5), h=30)
        for ii in OverSides():
            cmds.text(ii + '   ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_osface)
    if display4 != 0 and Num6 == 1:
        cmds.text('Ť����', bgc=(0.3, 0.4, 0.5), h=30)
        for ii in WrapFace():
            cmds.text(ii + '    ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_wpface)
    if display5 != 0 and Num7 == 1:
        cmds.text('���ű�', bgc=(0.3, 0.4, 0.5), h=30)
        for ii in OpenEdge():
            cmds.text(ii + '     ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_opedge)
    # Num8888888888888888888888888888
    if display7 != 0 and Num9 == 1:
        cmds.text('UV��ʧ', bgc=(0.3, 0.5, 0.4), h=30)
        for ii in UvLose():
            cmds.text(ii + '      ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_ulface)
    if display8 != 0 and Num10 == 1:
        cmds.text('UV�ص�', bgc=(0.3, 0.5, 0.4), h=30)
        for ii in UVoverlap():
            cmds.text(ii + '       ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_UVolface)
    if display9 != 0 and Num11 == 1:
        cmds.text('UV������', bgc=(0.3, 0.5, 0.4), h=30)
        for ii in UVout_Check():
            cmds.text(ii + '        ');
        cmds.button(label='ѡ��ȫ��', command=selectAll_outuv)
    if display10 != 0 and Num12 == 1:
        cmds.text('��β֡���', bgc=(0.6, 0.3, 0.4), h=30)
        cmds.text(AnKey_Check());
    if display11 != 0 and Num13 == 1:
        cmds.text('��ͼ�ߴ���', bgc=(0.5, 0.4, 0.3), h=30)
        for ii in Tex_Check():
            cmds.text(ii);        
    if display1 + display2 + display3 + display4 + display5 + display7 + display8 + display9 + display10 +display11== 0:
        cmds.text('���м��ͨ��')
# ѡ����ť
def selectAll_Axis(*args):
    cmds.select(AxisCheck())
def selectAll_Tran(*args):
    cmds.select(TransformCheck())
def selectAll_osface(*args):
    global osface
    cmds.select(osface)
def selectAll_wpface(*args):
    global wpface
    cmds.select(wpface)
def selectAll_opedge(*args):
    global opedge
    cmds.select(opedge)
def selectAll_ulface(*args):
    global ulface
    cmds.select(ulface)
def selectAll_UVolface(*args):
    global UVolface
    cmds.select(UVolface)
def selectAll_outuv(*args):
    global out
    cmds.select(out)


# ���尴ť
def checkBox_button(*args):
    global selection
    global Num1, Num2, Num3, Num4, Num5, Num6, Num7, Num8, Num9, Num10, Num11, Num12,Num13 
    global display1, display2, display3, display4, display5, display7, display8, display9,display10,display11
    display1 = display2 = display3 = display4 = display5 = display7 = display8 = display9 = display10 = display11 = 0
    # �洢ѡ������
    selection = cmds.ls(sl=True)
    cmds.select(clear=1)
    if Num1 == 1:
        UnitCheck();
    if Num2 == 1:
        FaceNum_Check();
    if Num3 == 1:
        AxisCheck();
    if Num4 == 1:
        TransformCheck()
    if Num5 == 1:
        OverSides()
    if Num6 == 1:
        WrapFace()
    if Num7 == 1:
        OpenEdge()
    # if Num8 == 1:
    # Hardedge_Check()
    if Num9 == 1:
        UvLose()
    if Num10 == 1:
        UVoverlap()
    if Num11 == 1:
        UVout_Check()
    if Num12 == 1:
        AnKey_Check()
    if Num13 == 1:
        Tex_Check()
    cmds.window(title='Check Reseult', w=300, h=500)
    cmds.scrollLayout(cr=True)
    cmds.frameLayout(label="Check Reseult")
    CheckReseult(*args)
    cmds.showWindow()


# make window
try:
    cmds.deleteUI(myWin)
except:
    pass

Num1 = Num2 = Num3 = Num4 = Num5 = Num6 = Num7 = Num8 = Num9 = Num10 = Num11 = Num12 = Num13= 0
display1 = display2 = display3 = display4 = display5 = display7 = display8 = display9 = display10 =display11 = 0

myWin = cmds.window(title='Check Panel v1.0', w=250, h=550)
col=cmds.columnLayout()
cmds.text(version + '���İ�');
cmds.setParent(col)

# Sense Check
cmds.frameLayout(label = "1:Sense Check",w=250,cll=True)
cmds.columnLayout()

cmds.checkBox('checkBox_Unit', label='��λ', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_Fc', label='����', v=0, cc='checkBoxs()')
fc = cmds.textFieldGrp(label='Limit  ',cw2=(40,50));

cmds.checkBox('checkBox_Texsize', label='��ͼ�ߴ�', v=0, cc='checkBoxs()')
size_field = cmds.textFieldGrp(label='Scale ', text="1024*1024", cw2=(40,80));
cmds.button(label='Get Scale', w=80, command=get_texsize)
cmds.button(label='Del Scale', w=80, command=del_texsize)
sco=cmds.textScrollList( h=60 )
cmds.separator( height=5, style='out' )
cmds.setParent(col)


# Mesh Check
cmds.frameLayout(label = "2:Mesh Check",w=250,cll=True)
cmds.columnLayout()
#cmds.checkBoxGrp( numberOfCheckBoxes=3, labelArray3=['���������', '����任', '�����'] ,cc='checkBoxs()')
cmds.checkBox('checkBox_Ax', label='���������', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_Ts', label='����任', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_Os', label='�����', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_Wf', label='Ť����', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_Oe', label='���ű�', v=0, cc='checkBoxs()')

cmds.setParent("..")
cmds.separator( height=5, style='out' )
cmds.setParent(col)
# cmds.checkBox( 'checkBox_He',label='Hardedge', v=0, cc='checkBoxs()' )

# UV Check
cmds.frameLayout(label = "3:UV Check",w=250,cll=True)
cmds.checkBox('checkBox_UVlose', label='UV��ʧ', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_UVoverlap', label='UV�ص�', v=0, cc='checkBoxs()')
cmds.checkBox('checkBox_UVOutside', label='UV������', v=0, cc='checkBoxs()')
#cmds.setParent("..")
cmds.separator( height=5, style='out' )
cmds.setParent(col)

# Animation Check
cmds.frameLayout(label = "4:Animation Check",w=250,cll=True)
cmds.checkBox('checkBox_Key', label='��β֡һ�£�ѡ����ǣ�', v=0, cc='checkBoxs()')
cmds.separator( height=5, style='out' )
cmds.setParent(col)

#Check Button
cmds.frameLayout(label = "Check Button",w=250,cll=False)
cmds.button(label="Check", w=200, h=50, command=checkBox_button, bgc=(0.3, 0.5, 0.4))
cmds.setParent("..")
cmds.separator( height=5, style='out' )
cmds.separator( height=5, style='out' )
cmds.showWindow(myWin)
