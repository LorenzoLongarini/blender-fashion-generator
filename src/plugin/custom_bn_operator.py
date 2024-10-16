import os
import math
import json
import datetime
import bpy


# global addon script variables
OUTPUT_TRAIN = 'train'
OUTPUT_TEST = 'test'
CAMERA_NAME = 'BlenderNeRF Camera'

import os
cwd = os.getcwd()
output_path = cwd + '/assets/output/'
print(output_path)

# blender nerf operator parent class
class BlenderNeRF_Operator(bpy.types.Operator):
    bl_idname = "object.blender_nerf_operator"
    bl_label = "BlenderNeRF Operator"
    # camera intrinsics
    def get_camera_intrinsics(self, scene, camera):
        camera_angle_x = camera.data.angle_x
        camera_angle_y = camera.data.angle_y

        # camera properties
        f_in_mm = camera.data.lens # focal length in mm
        scale = scene.render.resolution_percentage / 100
        width_res_in_px = scene.render.resolution_x * scale # width
        height_res_in_px = scene.render.resolution_y * scale # height
        optical_center_x = width_res_in_px / 2
        optical_center_y = height_res_in_px / 2

        # pixel aspect ratios
        size_x = scene.render.pixel_aspect_x * width_res_in_px
        size_y = scene.render.pixel_aspect_y * height_res_in_px
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y

        # sensor fit and sensor size (and camera angle swap in specific cases)
        if camera.data.sensor_fit == 'AUTO':
            sensor_size_in_mm = camera.data.sensor_height if width_res_in_px < height_res_in_px else camera.data.sensor_width
            if width_res_in_px < height_res_in_px:
                sensor_fit = 'VERTICAL'
                camera_angle_x, camera_angle_y = camera_angle_y, camera_angle_x
            elif width_res_in_px > height_res_in_px:
                sensor_fit = 'HORIZONTAL'
            else:
                sensor_fit = 'VERTICAL' if size_x <= size_y else 'HORIZONTAL'

        else:
            sensor_fit = camera.data.sensor_fit
            if sensor_fit == 'VERTICAL':
                sensor_size_in_mm = camera.data.sensor_height if width_res_in_px <= height_res_in_px else camera.data.sensor_width
                if width_res_in_px <= height_res_in_px:
                    camera_angle_x, camera_angle_y = camera_angle_y, camera_angle_x

        # focal length for horizontal sensor fit
        if sensor_fit == 'HORIZONTAL':
            sensor_size_in_mm = camera.data.sensor_width
            s_u = f_in_mm / sensor_size_in_mm * width_res_in_px
            s_v = f_in_mm / sensor_size_in_mm * width_res_in_px * pixel_aspect_ratio

        # focal length for vertical sensor fit
        if sensor_fit == 'VERTICAL':
            s_u = f_in_mm / sensor_size_in_mm * width_res_in_px / pixel_aspect_ratio
            s_v = f_in_mm / sensor_size_in_mm * width_res_in_px

        camera_intr_dict = {
            'camera_angle_x': camera_angle_x,
            'camera_angle_y': camera_angle_y,
            'fl_x': s_u,
            'fl_y': s_v,
            'k1': 0.0,
            'k2': 0.0,
            'p1': 0.0,
            'p2': 0.0,
            'cx': optical_center_x,
            'cy': optical_center_y,
            'w': width_res_in_px,
            'h': height_res_in_px,
            'aabb_scale': scene.aabb
        }

        return {'camera_angle_x': camera_angle_x} if scene.nerf else camera_intr_dict

    # camera extrinsics (transform matrices)
    def get_camera_extrinsics(self, scene, camera, mode='TRAIN'):
        assert mode == 'TRAIN' or mode == 'TEST'

        initFrame = scene.frame_current
        step = scene.frame_step
        if (mode == 'TRAIN'):
            end = scene.frame_start + scene.ttc_nb_frames - 1
        else:
            end = scene.frame_end

        camera_extr_dict = []
        for frame in range(scene.frame_start, end + 1, step):
            scene.frame_set(frame)
            filename = os.path.basename( scene.render.frame_path(frame=frame) )
            filedir = OUTPUT_TRAIN * (mode == 'TRAIN') + OUTPUT_TEST * (mode == 'TEST')

            frame_data = {
                'file_path': os.path.join(filedir, filename),
                'transform_matrix': self.listify_matrix(camera.matrix_world)
            }

            camera_extr_dict.append(frame_data)

        scene.frame_set(initFrame) # set back to initial frame

        return camera_extr_dict

    def save_json(self, directory, filename, data, indent=4):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=indent)

    def is_power_of_two(self, x):
        return math.log2(x).is_integer()

    # function from original nerf 360_view.py code for blender
    def listify_matrix(self, matrix):
        matrix_list = []
        for row in matrix:
            matrix_list.append(list(row))
        return matrix_list

    # assert messages
    def asserts(self, scene):

        train_camera = scene.camera_train_target
        test_camera = scene.camera_test_target

        ttc_name = scene.ttc_dataset_name

        error_messages = []

        if  not (train_camera.data.type == 'PERSP' and test_camera.data.type == 'PERSP'):
           error_messages.append('Only perspective cameras are supported!')

        if (ttc_name == ''):
            error_messages.append('Dataset name cannot be empty!')

        if not scene.nerf and not self.is_power_of_two(scene.aabb):
            error_messages.append('AABB scale needs to be a power of two!')

        if scene.save_path == '':
            scene.save_path =  output_path

        if scene.save_path == '':
            error_messages.append('Save path cannot be empty!')

        return error_messages

    def save_log_file(self, scene, directory, ):
        now = datetime.datetime.now()

        logdata = {
            'BlenderNeRF Version': scene.blendernerf_version,
            'Date and Time' : now.strftime("%d/%m/%Y %H:%M:%S"),
            'Train': scene.train_data,
            'Test': scene.test_data,
            'AABB': scene.aabb,
            'Render Frames': scene.render_frames,
            'File Format': 'NeRF' if scene.nerf else 'NGP',
            'Save Path': output_path,# scene.save_path,
            'Method': 'TTC'
        }

        logdata['Train Camera Name'] = scene.camera_train_target.name
        logdata['Test Camera Name'] = scene.camera_test_target.name
        logdata['Frames'] = scene.ttc_nb_frames
        logdata['Dataset Name'] = scene.ttc_dataset_name

        self.save_json(directory, filename='log.txt', data=logdata)