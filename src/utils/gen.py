import sys
import bpy
sys.path.append('./src/scene')
from init_scene import init_scene_prop

def gen_dataset(config, dataset_name,  ttc = True, seed = None):
    zip_file = init_scene_prop(bpy.context.scene, config, dataset_name, ttc=ttc, seed=seed)
    if ttc:
        bpy.ops.object.train_test_cameras()
    else:
        bpy.ops.object.camera_on_sphere()
    return zip_file