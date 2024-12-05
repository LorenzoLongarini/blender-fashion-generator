import bpy
import sys
import os
sys.path.append('./src/scene')
sys.path.append('./src/plugin')

from custom_bn_operator import BlenderNeRF_Operator
from custom_ttc_operator import TrainTestCameras
from custom_cos_operator import CameraOnSphere
from clean import clean_scene
from b_object import set_object
from cameras import create_camera
from lights import set_lights

FRAMES = [75, 230, 200]

# Register classes in Blender
def register():
    bpy.utils.register_class(BlenderNeRF_Operator)
    bpy.utils.register_class(TrainTestCameras)
    bpy.utils.register_class(CameraOnSphere)

# Unregister classes in Blender
# def unregister():
#     try:
#         bpy.utils.unregister_class(BlenderNeRF_Operator)
#         bpy.utils.unregister_class(TrainTestCameras)
#         print("Uneregister Success.")
#     except RuntimeError as e:
#         print(f"Unregister Error: {e}")


def unregister():
    for cls in [BlenderNeRF_Operator, TrainTestCameras, CameraOnSphere]:
        print("types:")
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
            print(f"Unregistered {cls.__name__} successfully.")
        else:
            print(f"{cls.__name__} not registered.")

def main():
    
    # Pulisci la scena esistente
    clean_scene()

    # Imposta le proprietà della scena
    initialize_scene_properties(bpy.context.scene)

    # Imposta l'oggetto Blender nella scena e ottieni l'oggetto importato
    obj = set_object(FRAMES[0], filepath='/assets/DeepFashion/2-1/')

    # Crea le telecamere e fai in modo che seguano l'oggetto
    create_camera(obj)

    # Imposta le luci ambientali
    # set_lights()


    # ttc plugin to create datasets
    # bpy.ops.object.train_test_cameras()
    bpy.ops.object.camera_on_sphere()


def initialize_scene_properties(scene, ttc=True):

    DATASET_NAME = "prova"


    output_path = os.getcwd() + '/assets/output/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    scene.aabb = 2  
    scene.nerf = True
    scene.train_data = True
    scene.test_data = False
    if ttc:
        scene.ttc_dataset_name = DATASET_NAME
    else:
        scene.cos_dataset_name = DATASET_NAME
    scene.save_path = output_path
    # scene.blendernerf_version = "1.0"  
    scene.render_frames = True
    scene.ttc_nb_frames = FRAMES[0]
    scene.frame_start = 1
    scene.frame_end = FRAMES[0]

# if __name__ == "__main__":
#     # initialize_scene_properties(bpy.context.scene)
#     unregister()
#     register()
#     main()


unregister()
register()
main()



