import bpy
from math import radians

def create_camera(target_obj):
    scn = bpy.context.scene

    # Distanza fissa dalle camere al centro dell'oggetto
    distance = 5  # Regola questa distanza per una visione migliore dell'oggetto

    # Crea la prima telecamera
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 35  # Lunghezza focale standard

    # Crea il primo oggetto telecamera
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    
    # Posiziona la telecamera fissa a una distanza fissa
    cam_obj1.location = (distance, -distance, distance / 2)  # Camera frontale
    cam_obj1.rotation_euler = (radians(45), 0, radians(45))  # Inclinazione della telecamera
    scn.collection.objects.link(cam_obj1)

    # Fai puntare la telecamera al centro dell'oggetto
    cam_obj1.constraints.new(type='TRACK_TO')
    cam_obj1.constraints['Track To'].target = target_obj
    cam_obj1.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'  # La camera guarda verso -Z
    cam_obj1.constraints['Track To'].up_axis = 'UP_Y'  # Asse positivo Y verso l'alto

    # Crea la seconda telecamera
    cam2 = bpy.data.cameras.new("Camera 2")
    cam2.lens = 35  # Lunghezza focale standard

    # Crea il secondo oggetto telecamera
    cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
    
    # Posiziona la seconda telecamera dall'altro lato, simmetrica alla prima
    cam_obj2.location = (-distance, distance, distance / 2)  # Camera posteriore
    cam_obj2.rotation_euler = (radians(45), 0, radians(-45))  # Inclinazione opposta rispetto alla prima
    scn.collection.objects.link(cam_obj2)

    # Fai puntare la seconda telecamera al centro dell'oggetto
    cam_obj2.constraints.new(type='TRACK_TO')
    cam_obj2.constraints['Track To'].target = target_obj
    cam_obj2.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
    cam_obj2.constraints['Track To'].up_axis = 'UP_Y'

    # Imposta la prima telecamera come attiva
    scn.camera = cam_obj1  # Se vuoi usare la seconda, puoi impostare cam_obj2