# python steps:
import bpy
import zipfile
import os.path
import os
import sys
import mathutils
# delete all objects in scene
for item in bpy.data.objects: item.select = True
bpy.ops.object.delete()

# start!
# unzip mhx2 zip
bpy.ops.wm.addon_refresh()
bpy.ops.wm.addon_enable(module="import_runtime_mhx2");
bpy.ops.wm.addon_enable(module="makeclothes");
bpy.ops.wm.addon_enable(module="maketarget");
bpy.ops.wm.addon_enable(module="makewalk");
bpy.data.scenes["Scene"].game_settings.material_mode='GLSL'
mhx2_file=os.getenv('mhx2')
animatons_file=os.getenv('animations')
output_blend=os.getenv('output')
bpy.ops.import_scene.makehuman_mhx2(filepath=mhx2_file)
added_items=[]
#######################################
fh = open(animatons_file, 'rb')
z = zipfile.ZipFile(fh)
for name in z.namelist():
    outpath = "/tmp/"
    print("Decompressing " + name + " on " + outpath)
    z.extract(name, outpath)
    bpy.ops.mcp.load_and_retarget(filepath=outpath+"/"+name)
    for element in bpy.data.actions:
        if element not in added_items:
            print("Adding "+element.name)
            element.name=os.path.splitext(name)[0]
            added_items.append(element)
            break

    # if loop in place:
    # fixate bone location
    # bpy.ops.mcp.fixate_bone()
    #bpy.ops.mcp.rescale_fcurves()
    #bpy.data.scenes["Scene"].McpLoopInPlace=True
    bpy.ops.mcp.loop_fcurves()
    bpy.ops.mcp.repeat_fcurves()
#######################################
bpy.data.objects[0].scale=mathutils.Vector((0.10000000000000, 0.10000000000000, 0.10000000000000))
# join in one geometry
# Change to GLSL


print("joining geometries....")

scene = bpy.context.scene
obs = []
for ob in scene.objects:
    # whatever objects you want to join...
    if ob.type == 'MESH':
        obs.append(ob)
ctx = bpy.context.copy()
# one of the objects to join
ctx['active_object'] = obs[0]
ctx['selected_objects'] = obs
# we need the scene bases as well for joining
ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]
bpy.ops.object.join(ctx)


bpy.ops.file.unpack_all()
bpy.ops.wm.save_as_mainfile(filepath=output_blend)
