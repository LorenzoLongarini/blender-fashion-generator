# import_object.py
import bpy
from math import radians
import os  

cwd = os.getcwd()

def import_obj(filepath):
    obj_path = ''
    for file in os.listdir(filepath):
        if file.endswith('.obj'):
            obj_path = filepath + file

    bpy.ops.wm.obj_import(filepath=obj_path)
    obj = bpy.context.selected_objects[0]
    print('Imported name: ', obj.name)
    return obj

def rotate_obj(obj, frame):

    # Initial location
    obj.location = (0, 0, 0)
    obj.rotation_euler = [radians(90), 0, 0]

    # Rotation on y axis only
    keyframes = [
        (1, [radians(90), 0, 0]),                   
        (frame//4, [radians(90), 0, radians(90)]),   
        (frame//2, [radians(90), 0, radians(180)]),  
        (3*frame//4, [radians(90), 0, radians(270)]),  
        (frame, [radians(90), 0, radians(360)])      
    ]
    
    # Set keyframes
    for frame_num, rotation in keyframes:
        obj.rotation_euler = rotation
        obj.keyframe_insert(data_path='rotation_euler', frame=frame_num)
        
    # Set interpolation for smoother rotation
    for fcurve in obj.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.handle_left_type = 'AUTO'
            kf.handle_right_type = 'AUTO'

def add_texture(obj, filepath):
    texture = ''
    for file in os.listdir(filepath):
        if file.endswith('.png'):
            texture = filepath + file

    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    
    if not mat.node_tree.nodes.get("Principled BSDF"):
        bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    else:
        bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(texture)
    
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # Set texture
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def set_object(frame, filepath = '/assets/DeepFashion/1-1/', ttc = True):
    print(cwd + filepath + 'model_cleaned.obj')
    obj = import_obj(filepath=cwd + filepath)
    add_texture(obj, filepath=cwd + filepath)

    # COS doesn't need rotation
    if ttc:
        rotate_obj(obj, frame)
    return obj  