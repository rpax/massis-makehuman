
import bpy
import zipfile
import os.path
import os
import sys
import mathutils
import fnmatch
import ntpath


def findfrec( directory , extension):
	matches = []
	for root, dirnames, filenames in os.walk(directory):
		for filename in fnmatch.filter(filenames, '*.'+extension):
			matches.append(os.path.join(root, filename))
	return matches

def clearscene( ):
	for item in bpy.data.objects: item.select = True
	bpy.ops.object.delete()

def prepareaddons():
	bpy.ops.wm.addon_refresh()
	bpy.ops.wm.addon_enable(module="import_runtime_mhx2");
	bpy.ops.wm.addon_enable(module="makeclothes");
	bpy.ops.wm.addon_enable(module="maketarget");
	bpy.ops.wm.addon_enable(module="makewalk");
	bpy.data.scenes["Scene"].game_settings.material_mode='GLSL'


def animfiles(gender):
	return findfrec("/animations/"+gender,'bvh')+findfrec("/animations/common/",'bvh')




for mhx2_file in findfrec("/input",'mhx2'):
	print("Processing "+mhx2_file)
	clearscene()
	prepareaddons()
	
	bpy.ops.import_scene.makehuman_mhx2(filepath=mhx2_file)
	added_items=[]
	for name in animfiles('male'):
		bpy.ops.mcp.load_and_retarget(filepath=name)
		for element in bpy.data.actions:
			if element not in added_items:
				print("Adding "+element.name)
				element.name=os.path.splitext(name)[0]
				added_items.append(element)
				break
	#bpy.ops.mcp.loop_fcurves()
	#bpy.ops.mcp.repeat_fcurves()
	bpy.data.objects[0].scale=mathutils.Vector((0.1000000, 0.100000, 0.100000))
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

	ftree="/".join(os.path.splitext(mhx2_file)[0].split('/')[2:])
	print("ftree: "+ftree)
	targetfolder = '/output/'+ ftree
	os.makedirs(targetfolder)
	blendfilename=ntpath.basename(mhx2_file).split('/')[0]+'.blend'
	print("bfn: "+blendfilename)
	bpy.ops.file.pack_all()
	bpy.ops.wm.save_as_mainfile(filepath=targetfolder+'/'+blendfilename)
	bpy.ops.file.unpack_all(method='WRITE_LOCAL')

#######################################



# join in one geometry











