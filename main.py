import bpy
# import time
import sys
sys.path.append('./src/scene')
# from src.utils import clear, import_obj, texture, cameras
from clear import clean_scene
from b_object import set_object
from cameras import create_camera

FRAMES = [75, 135, 200]

clean_scene()

create_camera()

set_object(FRAMES[0])

ciao


