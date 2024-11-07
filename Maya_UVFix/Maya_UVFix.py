# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.OpenMaya as om

def get_face_by_uvshellid(sids,sid):
    rfaces = []
    for i, value in enumerate(sids):
        if value == sid:
            rfaces.append(i)
    return rfaces

def get_filpuvshell(obj):
    tfaces=cmds.polyListComponentConversion(obj, tf=1)
    faces = cmds.ls(tfaces, fl=1)
    shell_ids = cmds.polyEvaluate(faces, uvShellIds=True)
    shell_result=[]
    for face in faces:
        uvs = []
        vtxFaces = cmds.ls(cmds.polyListComponentConversion(face,toVertexFace=True),flatten=True)
        for vtxFace in vtxFaces:
            uv = cmds.polyListComponentConversion(vtxFace,fromVertexFace=True,toUV=True)
            uvs.append( uv[0] )
        #get edge vectors and cross them to get the uv face normal
        uvAPos = cmds.polyEditUV(uvs[0], q=1)
        uvBPos = cmds.polyEditUV(uvs[1], q=1)
        uvCPos = cmds.polyEditUV(uvs[2], q=1)
        uvAB = om.MVector(uvBPos[0]-uvAPos[0], uvBPos[1]-uvAPos[1],0)
        uvBC = om.MVector(uvCPos[0]-uvBPos[0], uvCPos[1]-uvBPos[1],0)
        if (uvAB ^ uvBC) * om.MVector(0,0,1) > 0: uvnormal=1
        else: uvnormal=-1
        if uvnormal == -1:
            sid = cmds.polyEvaluate(face, uvShellIds=True)
            shell_result.append(sid[0])
    shell_result=list(set(shell_result))
    return shell_result,shell_ids


def onMayaDroppedPythonFile(*args):
    main()


def main():
    obj = cmds.ls(sl=True)[0]
    uvs,sids=get_filpuvshell(obj)
    for usid in uvs:
        fids=get_face_by_uvshellid(sids,usid)
        print(f"usid:{usid} {fids}")
        faces=[]
        for fid in fids:
            faces.append(f'{obj}.f[{fid}]')
        cmds.polyFlipUV(faces)
        #cmds.select(faces,add=True)
main()