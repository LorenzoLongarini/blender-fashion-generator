import bpy
from bpy import context
from math import radians
import os  
    
cwd = os.getcwd()

def import_obj(filepath = cwd + '/assets/DeepFashion/1-1/model_cleaned.obj'):
    # Verifica se il file esiste
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Il file .obj non esiste: {filepath}")
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
            break
    # Verifica se è stata trovata una texture
    if not texture:
        raise FileNotFoundError(f"Nessuna texture .png trovata nella directory: {filepath}")
    
    print(texture)
    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(texture)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def set_object(frame):
    obj = import_obj()  # Importa l'oggetto .obj
    add_texture(obj)    # Aggiungi la texture
    rotate_obj(obj, frame)  # Ruota l'oggetto con keyframes
    return obj  # Restituisci l'oggetto per l'utilizzo successivo