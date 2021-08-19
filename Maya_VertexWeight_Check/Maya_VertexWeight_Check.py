import maya.cmds as cmds

def getVertexWeights():
    
    sbs = []
    meshSkinCluster = None
    
    # get all selected vetices in order
    cmds.ConvertSelectionToVertices()
    verts = cmds.ls(flatten = True, orderedSelection = True)
    cmds.polyEvaluate( v=True)
    # check is any vertex 
    if len(verts) == 0:
        return cmds.error( "Please select vetices with skin weighs" )
    else:
        obj = cmds.ls(verts[0], objectsOnly = True)
        history = cmds.listHistory(obj) 
    #get mesh skin cluster
        for historyNode in history:
            if cmds.nodeType(historyNode)=="skinCluster":
                meshSkinCluster = historyNode
    #get joint list   
        for each in verts:
            #get weight values
            skinVals = cmds.skinPercent(meshSkinCluster, each, query=True, value=True)
            for v in skinVals:
                if( len(str(v)) >= 5 ):
                    sbs.append(each)
                    break
    r = len(sbs)
    if r>0:
        cmds.confirmDialog( title='PointCheck', message='Select bad point:'+str(r), button=['OK'], defaultButton='OK' )
        cmds.select(sbs)
    else:
        cmds.confirmDialog( title='PointCheck', message='No bad point!', button=['OK'], defaultButton='OK' )
getVertexWeights()
