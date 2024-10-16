
from math import radians
import bpy 
from bpy import context


def create_camera():
    scn = bpy.context.scene

    # create the first camera
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 18

    # create the first camera object
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    cam_obj1.location = (1.69, -1.85, 1.388)
    cam_obj1.rotation_euler = (0.6799, 0, 0.8254)
    scn.collection.objects.link(cam_obj1)

    # create the second camera
    cam2 = bpy.data.cameras.new("Camera 2")
    cam2.lens = 18

    # create the second camera object
    cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
    cam_obj2.location = (1.69, 1.85, 1.388)
    cam_obj2.rotation_euler = (radians(40.6), radians(-5.5), radians(140))
    scn.collection.objects.link(cam_obj2)