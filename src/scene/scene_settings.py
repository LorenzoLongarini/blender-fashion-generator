import bpy
from bpy import context
from mathutils import Vector
from math import radians 
import os  

cwd = os.getcwd()


def purge_orphans():
    override = bpy.context.copy()
    with context.temp_override(**override):
        bpy.ops.object.delete()


def clean_scene():
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # purge_orphans()

def set_lights():
    bpy.ops.object.light_add(type='SUN') 
    light = bpy.context.object
    light.name = "Sun light"
    light.location = (0, 0, 0) 
    light.data.energy = 5

    imported_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if imported_objects:
        obj = imported_objects[0]  
        print(f"Selected object: {obj.name}")

        light.location = (obj.location.x, obj.location.y, 10)
        direction = obj.location - light.location
        direction.normalize()
        light.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    else:
        print("No object selected!")

def create_camera(target_object, ttc):
    scn = bpy.context.scene


    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 50 
    cam1.type = 'PERSP'
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    cam_obj1.location = Vector((1.5, -1.5, 1.5)) 
    scn.collection.objects.link(cam_obj1)
    cam_obj1.rotation_euler[0] = radians(90)

    constraint1 = cam_obj1.constraints.new(type='TRACK_TO')
    constraint1.target = target_object  
    constraint1.track_axis = 'TRACK_NEGATIVE_Z'

    if ttc:
        cam2 = bpy.data.cameras.new("Camera 2")
        cam2.lens = 50  
        cam2.type = 'PERSP'
        cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
        cam_obj2.location = Vector((1.5, 1.0, 1.5))  
        scn.collection.objects.link(cam_obj2)
        cam_obj2.rotation_euler[0] = radians(90)  


        constraint2 = cam_obj2.constraints.new(type='TRACK_TO')
        constraint2.target = target_object 
        constraint2.track_axis = 'TRACK_NEGATIVE_Z'

    bpy.ops.object.select_all(action='DESELECT')
    cam_obj1.select_set(True)
    scn.camera = cam_obj1 
    scn.camera_train_target = cam_obj1
    if ttc:
        cam_obj2.select_set(True)
        scn.camera_test_target = cam_obj2


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