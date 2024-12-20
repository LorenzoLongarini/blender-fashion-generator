import sys
import bpy
sys.path.append('./src/plugin')
from custom_bn_operator import BlenderNeRF_Operator
from custom_ttc_operator import TrainTestCameras
from custom_cos_operator import CameraOnSphere

# Register classes in Blender
def register():
    bpy.utils.register_class(BlenderNeRF_Operator)
    bpy.utils.register_class(TrainTestCameras)
    bpy.utils.register_class(CameraOnSphere)

def unregister():
    for cls in [CameraOnSphere, TrainTestCameras, BlenderNeRF_Operator]:
        try:
            bpy.utils.unregister_class(cls)
        except:
            print('Error unregister class')
