from maya import cmds
from maya import OpenMaya
import os

def get_curve_shapes(curve_node):
    rshapes=[];
    d_shapes = cmds.listRelatives(curve_node, shapes=True, noIntermediate=True,f=1);
    for s in d_shapes:
        sty = cmds.nodeType(s);
        if sty != 'nurbsCurve':
            print(s+' is not a nurbsCurve');
            ncs = cmds.listRelatives(s, type='nurbsCurve');
            if ncs and len(ncs) > 0:
                rshapes.append(ncs);
        else:
            rshapes.append(s);
    return rshapes;

def create_root_uv_attribute(curves_group, mesh_node, uv_set='map1'):
    '''
    Create "groom_root_uv" attribute on group of curves.
    '''

    # check curves group
    if not cmds.objExists(curves_group):
        raise RuntimeError('Group not found: "{}"'.format(curves_group))

    # get curves in group
    final_shapes = [];
      
    nodes = cmds.listRelatives(curves_group,f=1);
    print(nodes);
    for node in nodes:
        rshapes = get_curve_shapes(node);
        if rshapes and len(rshapes) > 0:
            final_shapes+=rshapes;
            
    if not final_shapes or len(final_shapes) == 0:   
        raise RuntimeError('Invalid curves group. No nurbs-curves found in group.');
    else:
        print ("found curves " + str(len(final_shapes)) );
        #print (final_shapes)

    # get curve roots
    points = list()
    errCount = 0;
    for curve_shape in final_shapes:
        try:
            point = cmds.pointPosition('{}.cv[0]'.format(curve_shape), world=True)
            points.append(point);
        except Exception as err:
            raise RuntimeError('Invalid shape.'+str(err));
            #print("Error:"+ str(err));
            errCount = errCount+1;
    print("get {0} shapes,get {1} points".format(len(final_shapes),len(points)));

    # get uvs
    values = list()
    uvs = find_closest_uv_point(points, mesh_node, uv_set=uv_set)
    for u, v in uvs:
        values.append([u, v, 0])
        #print (str(u) + " , " + str(v)  )

    # create attribute
    name = 'groom_root_uv'
    cmds.addAttr(curves_group, ln=name, dt='vectorArray')
    cmds.addAttr(curves_group, ln='{}_AbcGeomScope'.format(name), dt='string')
    cmds.addAttr(curves_group, ln='{}_AbcType'.format(name), dt='string')

    cmds.setAttr('{}.{}'.format(curves_group, name), len(values), *values, type='vectorArray')
    cmds.setAttr('{}.{}_AbcGeomScope'.format(curves_group, name), 'uni', type='string')
    cmds.setAttr('{}.{}_AbcType'.format(curves_group, name), 'vector2', type='string')

    return uvs

def find_closest_uv_point(points, mesh_node, uv_set='map1'):
    '''
    Find mesh UV-coordinates at given points.
    '''

    # check mesh
    if not cmds.objExists(mesh_node):
        raise RuntimeError('Node not found: "{}"'.format(mesh_node))

    # check uv_set
    uv_sets = cmds.polyUVSet(mesh_node, q=True, allUVSets=True)
    if uv_set not in uv_sets:
        raise RuntimeError('Invalid uv_set provided: "{}"'.format(uv_set))

    # get mesh as dag-path
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(mesh_node)

    mesh_dagpath = OpenMaya.MDagPath()
    selection_list.getDagPath(0, mesh_dagpath)
    mesh_dagpath.extendToShape()

    # get mesh function set
    fn_mesh = OpenMaya.MFnMesh(mesh_dagpath)

    uvs = list()
    for i in range(len(points)):

        script_util = OpenMaya.MScriptUtil()
        script_util.createFromDouble(0.0, 0.0)
        uv_point = script_util.asFloat2Ptr()

        point = OpenMaya.MPoint(*points[i])
        fn_mesh.getUVAtPoint(point, uv_point, OpenMaya.MSpace.kWorld, uv_set)

        u = OpenMaya.MScriptUtil.getFloat2ArrayItem(uv_point, 0, 0)
        v = OpenMaya.MScriptUtil.getFloat2ArrayItem(uv_point, 0, 1)

        uvs.append((u, v))

    return uvs

def abc_export(filepath, node=None, start_frame=1, end_frame=1, data_format='otawa', uv_write=True):
    
    job_command = '-frameRange {} {} '.format(start_frame, end_frame)
    job_command += '-dataFormat {} '.format(data_format)
    
    job_command += '-attr groom_root_uv '

    if uv_write:
        job_command += '-uvWrite '
    
    job_command += '-root {} '.format(node)   
    
    job_command += '-file {} '.format(filepath) 
    
    cmds.AbcExport(verbose=True, j=job_command)
    
    


def main():
    
    export_directory = 'D:/Dev/Ref'
    hair_file = os.path.join(export_directory, 'hair_export.abc')
    curve_top_group = '|cat_hair_groom_textA_25_3:descriptionCAT_splineDescription'
    uv_mesh='body:body'
    
    create_root_uv_attribute( curve_top_group , uv_mesh)
    abc_export(hair_file, curve_top_group)
    
main()
