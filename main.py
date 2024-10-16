import bpy
from math import radians
import sys
import os
sys.path.append('./src/scene')
sys.path.append('./src/plugin')

from custom_bn_operator import BlenderNeRF_Operator
from custom_ttc_operator import TrainTestCameras
from clean import clean_scene
from b_object import set_object
from cameras import create_camera
from lights import set_lights

FRAMES = [75, 135, 200]

# Register classes in Blender
def register():
    bpy.utils.register_class(BlenderNeRF_Operator)
    bpy.utils.register_class(TrainTestCameras)

# Unregister classes in Blender
def unregister():
    try:
        bpy.utils.unregister_class(BlenderNeRF_Operator)
        bpy.utils.unregister_class(TrainTestCameras)
        print("Unregister Success.")
    except RuntimeError as e:
        print(f"Unregister Error: {e}")

def main():
    clean_scene()

    # Imposta l'oggetto nella scena e ottieni l'oggetto creato
    obj = set_object(FRAMES[0])

    # Imposta le telecamere e passagli l'oggetto che devono puntare
    create_camera(obj)

    # Imposta le luci
    set_lights()

def initialize_scene_properties(scene):
    output_path = os.getcwd() + '/assets/output/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    scene.aabb = 2  
    scene.nerf = False
    scene.train_data = True
    scene.test_data = True
    scene.ttc_dataset_name = "train"
    scene.save_path = output_path
    scene.render_frames = True
    scene.ttc_nb_frames = 75
    scene.frame_start = 1
    scene.frame_end = 75

initialize_scene_properties(bpy.context.scene)
unregister()
register()
main()