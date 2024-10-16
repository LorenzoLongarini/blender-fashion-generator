import bpy
from bpy import context
from math import radians
import os

# Ottieni la directory di lavoro corrente
cwd = os.getcwd()

def import_obj(filepath=cwd + '/assets/DeepFashion/1-1/model_cleaned.obj'):
    # Verifica se il file esiste
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Il file .obj non esiste: {filepath}")
    
    print(f"Importando l'oggetto da: {filepath}")
    
    # Importa l'oggetto
    bpy.ops.wm.obj_import(filepath=filepath)
    
    # Assumi che il primo oggetto selezionato sia quello importato
    obj = bpy.context.selected_objects[0]
    print('Nome importato: ', obj.name)
    return obj
   
def rotate_obj(obj, frame):
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    
    # Inserisci un keyframe per la rotazione iniziale
    obj.keyframe_insert(data_path='rotation_euler', frame=1)
    
    # Rotazione finale
    obj.rotation_euler = (radians(45), radians(45), radians(45))
    
    # Inserisci un keyframe per la rotazione finale
    obj.keyframe_insert(data_path='rotation_euler', frame=frame)

def add_texture(obj, filepath=cwd + '/assets/DeepFashion/1-1/'):
    texture = ''
    
    # Trova il file della texture (assume che ci sia un file PNG)
    for file in os.listdir(filepath):
        if file.endswith('.png'):
            texture = os.path.join(filepath, file)  # Usa os.path.join per creare il percorso completo
            break  # Esci dal ciclo non appena trovi una texture
    
    if not texture:
        print("Nessuna texture trovata nella directory:", filepath)
        return
    
    print("Texture trovata:", texture)
    
    # Crea un nuovo materiale
    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    
    # Aggiungi i nodi del materiale
    bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)  # Posizione del nodo per migliorare la leggibilità
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(texture)
    texImage.location = (-300, 0)  # Posizione del nodo della texture
    
    # Collega la texture al nodo Principled BSDF
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    
    # Assegna il materiale all'oggetto
    if obj.data.materials:
        obj.data.materials[0] = mat  # Sostituisce il primo materiale
    else:
        obj.data.materials.append(mat)  # Aggiunge il materiale se non esiste
    
    print(f"Materiale e texture applicati all'oggetto: {obj.name}")

def set_object(frame):
    obj = import_obj()  # Importa l'oggetto .obj
    add_texture(obj)    # Aggiungi la texture
    rotate_obj(obj, frame)  # Ruota l'oggetto con keyframes
    return obj  # Restituisci l'oggetto per l'utilizzo successivo