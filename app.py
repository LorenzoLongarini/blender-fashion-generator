import sys
import os
# from dotenv import load_dotenv

sys.path.append('./src/scene')
sys.path.append('./src/utils')

from config import load_config
from register_blender import register, unregister
from folder_transform import dataset_manager
from gen import gen_dataset
from scene_settings import clean_scene, set_object, create_camera, set_lights
from init_scene import init_bpy_prop

# load_dotenv()

def set_and_gen(config, output_path):
    train_name = config.get('train_name')
    test_name = config.get('test_name')
    lights = config.get('lights')
    ttc = config.get('ttc')
    frames = config.get('frames')
    asset_path = config.get('asset_path')
    hd = config.get("hd")
    focal = config.get('focal')

    clean_scene()
    obj = set_object(frames, filepath=asset_path)

    # cos does not need cameras init
    # if ttc:
    create_camera(obj, ttc, focal = focal)

    if lights:
        print("il valore di lights è settato a: ", lights)
        set_lights()
    init_bpy_prop(hd)
    
    # generate dataset twice
    if ttc: 
        file_zip = gen_dataset(config, f'{train_name}', ttc = ttc)
        return file_zip, ''

    train_zip = gen_dataset(config, f'train_{train_name}', ttc = ttc, seed = 0)
    while(True):
        print(os.listdir(output_path))
        if any(file.endswith('.zip') and 'train' in file for file in os.listdir(output_path)):
            break
    test_zip = gen_dataset(config, f'test_{test_name}', ttc = ttc)
    return train_zip, test_zip

def app():  
    cwd = os.getcwd()
    output_path = "/assets/output"

    output_path = cwd + output_path

    config = load_config('config.json')

    unregister()
    register()

    train_zip, test_zip = set_and_gen(config, output_path)
    print(train_zip, test_zip)

    ttc = config.get('ttc')
    dataset_manager(f'{output_path}/{train_zip}', f'{output_path}/{test_zip}', ttc)


app()
# if __name__ == "__main__":
#     main()
