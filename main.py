import bpy
from bpy import context
import sys
sys.path.append('..src/utils')
from clear import clean_scene

# bpy.ops.scene.delete()
# bpy.ops.scene.new(type="NEW")

clean_scene()
path = 'D:/DeepFashion/1-1/model_cleaned.obj'
imported_object = bpy.ops.wm.obj_import(filepath=path)
obj_object = bpy.context.selected_objects[0]
print('Imported name: ', obj_object.name)

mat = bpy.data.materials.new(name="New_Mat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = bpy.data.images.load("D:/DeepFashion/1-1/1-1_tex.png")
mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

ob = context.view_layer.objects.active

# Assign it to object
if ob.data.materials:
    ob.data.materials[0] = mat
else:
    ob.data.materials.append(mat)