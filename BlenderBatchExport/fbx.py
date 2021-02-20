import bpy
import os
import sys
import argparse

def RemoveCollection(colname='Collection'):
    coll = bpy.data.collections.get(colname);
    if coll:
        obs = [o for o in coll.objects if o.users == 1]
        while obs:
            bpy.data.objects.remove(obs.pop());
        bpy.data.collections.remove(coll);
    else :
        print("Can not get " + colname);

if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', dest='source', metavar='FILE');
    args = parser.parse_known_args(argv)[0]
    # print parameters
    print('source file: ', args.source);
    RemoveCollection();
    (folderpath, filename) = os.path.split(args.source);
    (filename, ext) = os.path.splitext(filename);
    # print(filename)
    # print(folderpath)
    bpy.ops.import_scene.gltf(filepath=args.source);
    bpy.ops.export_scene.fbx(filepath= os.path.join(folderpath,filename+".fbx"));
    