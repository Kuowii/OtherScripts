import maya.cmds as cmds

theNodes = cmds.ls(dag = True, s = True,type="shape");
mb=cmds.ls(type='shadingEngine');
fss=cmds.ls(type='file');

def test(info):
    print(info);

def newNormalMat(m):
    nBlinn = 'bl_'+m;
    sg = nBlinn+'_SG';
    nBlinn = cmds.shadingNode('blinn', asShader=True,n=nBlinn);
    sg=cmds.sets(renderable=1,noSurfaceShader=1,empty=1,name=nBlinn+'_SG');
    cmds.connectAttr( nBlinn + ".outColor",sg + ".surfaceShader",force=1);
    bc = m.replace("_mt", "_b");
    bn = m.replace("_mt","_n");
    
    if bc in fss:
        cmds.connectAttr(bc+'.outColor',nBlinn+'.color', force=True);
    else: 
        print(bc+" not found.");
    
    if bn in fss:
        cmds.connectAttr(bn+'.outColor',nBlinn+'.normalCamera', force=True);
    else: 
        print(bn+" not found.");
    
    return [nBlinn,sg];

for n in theNodes: 
    shadeEng = cmds.listConnections(n , type = "shadingEngine");
    materials = cmds.ls(cmds.listConnections(shadeEng ), materials = True);
    for m in materials:
        if m.startswith('bl_'):continue;
        nBlinn = 'bl_'+m;
        sg = nBlinn+'_SG';
        if nBlinn not in mb:
            se = newNormalMat(m);
            nBlinn = se[0];
            sg = se[1];
            mb.append(nBlinn);
        cmds.select(cl=True);       
        cmds.select(n);
        cmds.hyperShade( nBlinn, assign=sg );

print("Set Over");