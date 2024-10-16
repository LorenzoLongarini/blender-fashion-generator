import bpy
from math import radians

def calculate_distance_for_camera(obj, camera_fov=50):
    """Calcola la distanza ottimale per la telecamera in base al bounding box dell'oggetto."""
    # Ottieni il bounding box dell'oggetto
    bbox_corners = [obj.matrix_world @ corner for corner in obj.bound_box]
    
    # Trova le dimensioni massime dell'oggetto
    max_dimension = max((bbox_corners[0] - bbox_corners[6]).length, (bbox_corners[1] - bbox_corners[7]).length)
    
    # Converti l'angolo di visuale (fov) in radianti e calcola la distanza ideale
    fov_radians = radians(camera_fov)
    distance = (max_dimension / 2) / (radians(fov_radians / 2))

    return distance

def create_camera(target_obj):
    scn = bpy.context.scene

    # Calcola la distanza dinamica basata sull'oggetto
    distance = calculate_distance_for_camera(target_obj)

    # create the first camera
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 35  # Questa può essere regolata dinamicamente, ma iniziamo con 35 mm

    # create the first camera object
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    
    # Posiziona la camera a distanza calcolata dall'oggetto
    cam_obj1.location = (distance, -distance, distance / 2)
    cam_obj1.rotation_euler = (radians(45), 0, radians(45))  # Ruota la camera verso l'oggetto
    scn.collection.objects.link(cam_obj1)

    # Fai puntare la telecamera all'oggetto
    cam_obj1.constraints.new(type='TRACK_TO')
    cam_obj1.constraints['Track To'].target = target_obj
    cam_obj1.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
    cam_obj1.constraints['Track To'].up_axis = 'UP_Y'

    # create the second camera
    cam2 = bpy.data.cameras.new("Camera 2")
    cam2.lens = 35  # Anche qui, se vuoi, può essere regolata dinamicamente

    # create the second camera object
    cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
    
    # Posiziona la seconda camera dall'altro lato
    cam_obj2.location = (-distance, distance, distance / 2)
    cam_obj2.rotation_euler = (radians(45), 0, radians(-45))  # Ruota la camera verso l'oggetto
    scn.collection.objects.link(cam_obj2)

    # Fai puntare la seconda camera all'oggetto
    cam_obj2.constraints.new(type='TRACK_TO')
    cam_obj2.constraints['Track To'].target = target_obj
    cam_obj2.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
    cam_obj2.constraints['Track To'].up_axis = 'UP_Y'