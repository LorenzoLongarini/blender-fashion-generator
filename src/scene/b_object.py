# import_object.py
import bpy
from math import radians
import os  

cwd = os.getcwd()

def import_obj(filepath=cwd + '/assets/DeepFashion/1-1/model_cleaned.obj'):
    print(filepath)
    bpy.ops.wm.obj_import(filepath=filepath)
    obj = bpy.context.selected_objects[0]
    print('Imported name: ', obj.name)
    return obj

def rotate_obj(obj, frame):
    # Resetta la posizione e rotazione iniziale
    obj.location = (0, 0, 0)
    obj.rotation_euler = [0, 0, 0]
    # obj.keyframe_insert(data_path='rotation_euler', frame=1)
    # obj.rotation_euler = [radians(45), radians(45), radians(45)]
    # obj.keyframe_insert(data_path='rotation_euler', frame=frame)
    
    # Crea più keyframes per una rotazione più fluida
    keyframes = [
        (1, [0, 0, 0]),                    # Inizio
        (frame//4, [0, 0, radians(90)]),   # 1/4 rotazione
        (frame//2, [0, radians(45), radians(180)]),  # Metà rotazione
        (3*frame//4, [radians(30), radians(45), radians(270)]),  # 3/4 rotazione
        (frame, [0, 0, radians(360)])      # Rotazione completa
    ]
    
    # Imposta i keyframes
    for frame_num, rotation in keyframes:
        obj.rotation_euler = rotation
        obj.keyframe_insert(data_path='rotation_euler', frame=frame_num)
        
    # Imposta l'interpolazione per una rotazione più fluida
    for fcurve in obj.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.handle_left_type = 'AUTO'
            kf.handle_right_type = 'AUTO'

def add_texture(obj, filepath=cwd + '/assets/DeepFashion/1-1/'):
    texture = ''
    for file in os.listdir(filepath):
        if file.endswith('.png'):
            texture = filepath + file
    print(texture)

    # Crea un nuovo materiale
    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    
    # Assicurati che il nodo Principled BSDF esista
    if not mat.node_tree.nodes.get("Principled BSDF"):
        bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    else:
        bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Aggiungi un nodo di immagine
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(texture)
    
    # Collega il nodo immagine al nodo BSDF
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # Assegna il materiale all'oggetto
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def set_object(frame):
    obj = import_obj()
    add_texture(obj)
    rotate_obj(obj, frame)
    return obj  # Restituisce l'oggetto importato per utilizzarlo altrove