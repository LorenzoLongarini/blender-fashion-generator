import bpy
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
        print("Uneregister Success.")
    except RuntimeError as e:
        print(f"Unregister Error: {e}")

def main():
    
    # Pulisci la scena esistente
    clean_scene()

    # Imposta le proprietà della scena
    initialize_scene_properties(bpy.context.scene)

    # Imposta l'oggetto Blender nella scena e ottieni l'oggetto importato
    obj = set_object(FRAMES[0])

    # Crea le telecamere e fai in modo che seguano l'oggetto
    create_camera(obj)

    # Imposta le luci ambientali
    set_lights()


    # ttc plugin to create datasets
    bpy.ops.object.train_test_cameras()


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
    # scene.blendernerf_version = "1.0"  
    scene.render_frames = True
    scene.ttc_nb_frames = 75
    scene.frame_start = 1
    scene.frame_end = 75



initialize_scene_properties(bpy.context.scene)
unregister()
register()
main()



