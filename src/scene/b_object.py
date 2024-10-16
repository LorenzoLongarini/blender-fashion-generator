import bpy
from bpy import context
from math import radians
def import_obj():
    # filepath = 'D:/DeepFashion/1-1/model_cleaned.obj'
    filepath = '/Users/alerong/Downloads/Computer Graphics/Dataset/filtered_registered_mesh-001/1-1'
    bpy.ops.wm.obj_import(filepath=filepath)
    obj = bpy.context.selected_objects[0]
    print('Imported name: ', obj.name)
    return obj
   
def rotate_obj(obj, frame):
    obj.rotation_euler = [0, 0, 0]
    obj.keyframe_insert(data_path = 'rotation_euler', frame = 1)
    obj.rotation_euler = [radians(45), radians(45), radians(45)]
    obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)


def add_texture(obj):
    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load("/Users/alerong/Downloads/Computer Graphics/Dataset/filtered_registered_mesh-001/1-1/1-1_tex.png")
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
