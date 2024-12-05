import bpy
import sys
import os
import time
sys.path.append('./src/scene')
sys.path.append('./src/plugin')

from custom_bn_operator import BlenderNeRF_Operator
from custom_ttc_operator import TrainTestCameras
from custom_cos_operator import CameraOnSphere
from clean import clean_scene
from b_object import set_object
from cameras import create_camera
from lights import set_lights
import zipfile

FRAMES = [75, 230, 200]

def unzip_and_remove(zip_filepath, extract_to):

    # Controlla se il file ZIP esiste
    if not os.path.exists(zip_filepath):
        print(f"Il file {zip_filepath} non esiste.")
        return

    # Crea la directory di estrazione se non esiste
    os.makedirs(extract_to, exist_ok=True)

    # Estrai il file ZIP
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"File estratti in {extract_to}")

    # Rimuovi il file ZIP
    os.remove(zip_filepath)
    print(f"File ZIP {zip_filepath} rimosso.")

# Register classes in Blender
# def register():
#     bpy.utils.register_class(BlenderNeRF_Operator)
#     bpy.utils.register_class(TrainTestCameras)
#     bpy.utils.register_class(CameraOnSphere)
def register():
    for cls in [BlenderNeRF_Operator, TrainTestCameras, CameraOnSphere]:
        if not hasattr(bpy.types, cls.__name__):
            bpy.utils.register_class(cls)
        else:
            print(f"{cls._name_} is already registered.")


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

def gen(dataset_name = "train", ttc = True):
    initialize_scene_properties(bpy.context.scene, dataset_name, ttc=ttc)
    print(dataset_name)
    if ttc:
        bpy.ops.object.train_test_cameras()
    else:
        bpy.ops.object.camera_on_sphere()


def main():
    
    # Pulisci la scena esistente
    clean_scene()


    # Imposta l'oggetto Blender nella scena e ottieni l'oggetto importato
    obj = set_object(FRAMES[0], filepath='/assets/DeepFashion/2-1/')

    # Crea le telecamere e fai in modo che seguano l'oggetto
    create_camera(obj)

    # Imposta le luci ambientali
    # set_lights()
    gen(dataset_name = "trainNerf", ttc = False)
    time.sleep(60)
    gen(dataset_name = "testNerf", ttc = False)

    # initialize_scene_properties(bpy.context.scene, dataset_name = "train")
    # ttc plugin to create datasets
    # bpy.ops.object.train_test_cameras()
    # for i in ["train", "test"]:
    # Imposta le proprietà della scena
    # bpy.ops.object.camera_on_sphere()

    # initialize_scene_properties(bpy.context.scene, dataset_name = "test")
    # bpy.ops.object.camera_on_sphere()


def initialize_scene_properties(scene, dataset_name = "prova", ttc=False, seed = 0):
    print(dataset_name, ttc)

    output_path = os.getcwd() + '/assets/output/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    scene.aabb = 2  
    scene.nerf = True
    scene.train_data = True
    scene.test_data = False
    if ttc:
        scene.ttc_dataset_name = dataset_name
    else:
        scene.cos_dataset_name = dataset_name
        scene.seed = seed
    scene.save_path = output_path
    # scene.blendernerf_version = "1.0"  
    scene.render_frames = True
    scene.ttc_nb_frames = FRAMES[0]
    scene.frame_start = 1
    scene.frame_end = FRAMES[0]

if __name__ == "__main__":
    # initialize_scene_properties(bpy.context.scene)
    # unregister()
    # register()
    # main()
    zip_filepath = os.getcwd() + '/assets/output/' +  "trainNerf" + ".zip"# Sostituisci con il percorso del tuo file ZIP
    extract_to = os.getcwd() + '/assets/output/' +  "trainNerf"  # Sostituisci con la directory di estrazione desiderata

    unzip_and_remove(zip_filepath, extract_to)


# unregister()
# register()
# main()


