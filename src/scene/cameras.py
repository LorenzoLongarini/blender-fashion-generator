# create_cameras.py
import bpy
from mathutils import Vector
from math import radians  # Assicurati di importare la funzione radians

def create_camera(target_object):
    scn = bpy.context.scene

    # Creazione della prima telecamera
    cam1 = bpy.data.cameras.new("Camera 1")

    #Lollo
    # cam1.lens = 18
    # cam1.type = 'PERSP'
    # # create the first camera object
    # cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    # # cam_obj1.location = (1.69, -1.85, 1.388)
    # # cam_obj1.rotation_euler = (0.6799, 0, 0.8254)
    # cam_obj1.location = (0.0, 0.0, 1.0)
    # cam_obj1.rotation_euler = (radians(45), 0, 0)
    # scn.collection.objects.link(cam_obj1)

    # # create the second camera
    # cam2 = bpy.data.cameras.new("Camera 2")
    # cam2.lens = 18
    # cam2.type = 'PERSP'

    # # create the second camera object
    # cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
    # # cam_obj2.location = (1.69, 1.85, 1.388)
    # # cam_obj2.rotation_euler = (radians(40.6), radians(-5.5), radians(140))
    # cam_obj1.location = (2.0, 0.0, 1.5)
    # cam_obj1.rotation_euler = (radians(45), radians(90), 0)
    # scn.collection.objects.link(cam_obj2)

    #  # Deselect all objects first
    # bpy.ops.object.select_all(action='DESELECT')
    
    # # Seleziona entrambe le telecamere
    # cam_obj1.select_set(True)
    # cam_obj2.select_set(True)

    # Imposta la prima telecamera come attiva (opzionale)
    # scn.camera = cam_obj1

    # Imposta le telecamere nella scena come train e test
    # scn.camera_train_target = cam_obj1
    # scn.camera_test_target = cam_obj2

    cam1.lens = 50  # Aumenta la lunghezza focale per il zoom (da 18 a 50 mm)
    cam1.type = 'PERSP'
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)

    # Posizione della prima telecamera
    cam_obj1.location = Vector((2.0, -2.0, 1.5))  # Posizione iniziale
    scn.collection.objects.link(cam_obj1)

    # Aggiungi un'ulteriore rotazione di 90 gradi attorno all'asse X
    cam_obj1.rotation_euler[0] = radians(90)  # Imposta direttamente a 90 gradi

    # Creazione della seconda telecamera
    cam2 = bpy.data.cameras.new("Camera 2")
    cam2.lens = 50  # Aumenta la lunghezza focale per il zoom (da 18 a 50 mm)
    cam2.type = 'PERSP'
    cam_obj2 = bpy.data.objects.new("Camera 2", cam2)

    # Posizione della seconda telecamera
    cam_obj2.location = Vector((-2.0, 2.0, 1.5))  # Posizione iniziale
    scn.collection.objects.link(cam_obj2)

    # Aggiungi un'ulteriore rotazione di 90 gradi attorno all'asse X per la seconda telecamera
    cam_obj2.rotation_euler[0] = radians(90)  # Imposta direttamente a 90 gradi

    # Aggiungi un constraint di tipo "Track To" alle telecamere
    constraint1 = cam_obj1.constraints.new(type='TRACK_TO')
    constraint1.target = target_object  # Oggetto centrale
    constraint1.track_axis = 'TRACK_NEGATIVE_Z'  # Punta lungo l'asse negativo Z

    constraint2 = cam_obj2.constraints.new(type='TRACK_TO')
    constraint2.target = target_object  # Oggetto centrale
    constraint2.track_axis = 'TRACK_NEGATIVE_Z'  # Punta lungo l'asse negativo Z

    # Deseleziona tutti gli oggetti
    bpy.ops.object.select_all(action='DESELECT')
    
    # Seleziona entrambe le telecamere
    cam_obj1.select_set(True)
    cam_obj2.select_set(True)

    # Imposta la prima telecamera come attiva
    scn.camera = cam_obj1  # Puoi anche cambiare tra le telecamere come necessario

    # Assegna i target per la telecamera train e test
    scn.camera_train_target = cam_obj1
    scn.camera_test_target = cam_obj2
