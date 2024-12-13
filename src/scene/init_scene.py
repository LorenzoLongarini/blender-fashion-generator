import os
import bpy

def init_scene_prop(scene, config, dataset_name, ttc=False, seed = None):
    # get config data
    frames = config.get('frames')
    focal = config.get('focal')
    sphere_scale = config.get('sphere_scale')
    sphere_radius = config.get('sphere_radius')
    aabb = config.get('aabb')
    nerf = config.get('nerf')
    light = config.get('lights')

    is_nerf = '_nerf' if nerf else 'ngp'
    is_light = '_light' if light else ''
    
    #create output path
    output_path = os.getcwd() + '/assets/output/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    zip_path = ''
    #initialize scene properties
    scene.aabb = aabb  
    scene.nerf = nerf
    scene.train_data = True
    scene.test_data = False
    scene.frame_start = 1
    scene.frame_end = frames
    scene.save_path = output_path
    scene.render_frames = True
    # scene.blendernerf_version = "1.0"  

    if ttc:
        zip_path = f'TTC_{dataset_name}_{frames}F{is_nerf}{is_light}'
        scene.ttc_dataset_name = zip_path
        scene.ttc_nb_frames = frames
    else:
        zip_path = f'COS_{dataset_name}_{frames}F{is_nerf}{is_light}'
        scene.cos_dataset_name = zip_path
        print("il valore di seed è ", seed)
        scene.seed = seed if seed is not None else config.get('seed')
        scene.sphere_scale = sphere_scale
        scene.focal = focal
        scene.sphere_radius = sphere_radius
        scene.cos_nb_frames = frames
    
    return zip_path

def init_bpy_prop():
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    #remove comment to high resolution
    # bpy.context.scene.cycles.samples = 128
    # bpy.context.scene.cycles.use_denoising = True
    # bpy.context.scene.render.resolution_x = 3840
    # bpy.context.scene.render.resolution_y = 2160