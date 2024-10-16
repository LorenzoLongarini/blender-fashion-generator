import bpy
from bpy import context
from math import radians
import os  
    
cwd = os.getcwd()

def import_obj(filepath = cwd + '/assets/DeepFashion/1-1/model_cleaned.obj'):
    print(filepath)
    bpy.ops.wm.obj_import(filepath=filepath)
    obj = bpy.context.selected_objects[0]
    print('Imported name: ', obj.name)
    return obj
   
def rotate_obj(obj, frame):
    obj.location = (0, 0, 0)
    obj.rotation_euler = [0, 0, 0]
    obj.keyframe_insert(data_path = 'rotation_euler', frame = 1)
    obj.rotation_euler = [radians(45), radians(45), radians(45)]
    obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)


def add_texture(obj, filepath =  cwd + '/assets/DeepFashion/1-1/'):
    texture = ''
    for file in os.listdir(filepath):
        if file.endswith('.png'):
            texture = filepath + file
    print(texture)
    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(texture)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # ob = context.view_layer.objects.active

    # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def set_object(frame):
    obj = import_obj()
    add_texture(obj)
    rotate_obj(obj, frame)
