
from math import radians
import bpy 
from bpy import context


def create_camera():
    scn = bpy.context.scene

    # create the first camera
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 18
    cam1.type = 'PERSP'
    # create the first camera object
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    # cam_obj1.location = (1.69, -1.85, 1.388)
    # cam_obj1.rotation_euler = (0.6799, 0, 0.8254)
    cam_obj1.location = (0.0, 0.0, 1.0)
    cam_obj1.rotation_euler = (radians(45), 0, 0)
    scn.collection.objects.link(cam_obj1)

    # create the second camera
    cam2 = bpy.data.cameras.new("Camera 2")
    cam2.lens = 18
    cam2.type = 'PERSP'

    # create the second camera object
    cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
    # cam_obj2.location = (1.69, 1.85, 1.388)
    # cam_obj2.rotation_euler = (radians(40.6), radians(-5.5), radians(140))
    cam_obj1.location = (2.0, 0.0, 1.5)
    cam_obj1.rotation_euler = (radians(45), radians(90), 0)
    scn.collection.objects.link(cam_obj2)

     # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Seleziona entrambe le telecamere
    cam_obj1.select_set(True)
    cam_obj2.select_set(True)

    # Imposta la prima telecamera come attiva (opzionale)
    # scn.camera = cam_obj1

    # Imposta le telecamere nella scena come train e test
    scn.camera_train_target = cam_obj1
    scn.camera_test_target = cam_obj2

