import bpy
# import time
import sys
sys.path.append('./src/scene')
sys.path.append('./src/plugin')
# from src.utils import clear, import_obj, texture, cameras
from custom_bn_operator import BlenderNeRF_Operator
from custom_ttc_operator import TrainTestCameras
from clear import clean_scene
from b_object import set_object
from cameras import create_camera

# Registrazione delle classi in Blender
def register():
    bpy.utils.register_class(BlenderNeRF_Operator)
    bpy.utils.register_class(TrainTestCameras)

# Deregistrazione delle classi in Blender
def unregister():
    bpy.utils.unregister_class(BlenderNeRF_Operator)
    bpy.utils.unregister_class(TrainTestCameras)

def main():
    FRAMES = [75, 135, 200]

    clean_scene()

    create_camera()

    set_object(FRAMES[0])
    train_test_cameras_op = bpy.ops.object.train_test_cameras()
    # TrainTestCameras()
    
    # Esegui l'operatore (dovrai passare un context appropriato, qui uso un placeholder)
    context = bpy.context
    train_test_cameras_op.execute(context)

import os
cwd = os.getcwd()
output_path = cwd + '/assets/output'
print(output_path)

def initialize_scene_properties(scene):
    scene.aabb = 2  # esempio di valore, assicurati che sia una potenza di due se necessario
    scene.nerf = False  # oppure True, a seconda di ciò che ti serve
    scene.train_data = True
    scene.test_data = True
    scene.ttc_dataset_name = "Example Dataset"
    scene.save_path = output_path
    # scene.blendernerf_version = "1.0"  # o qualsiasi altra versione
    scene.render_frames = True
    scene.ttc_nb_frames = 75
    scene.frame_start = 1
    scene.frame_end = 250

unregister()
register()
initialize_scene_properties(bpy.context.scene)
main()



