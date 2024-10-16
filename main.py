# main.py

import bpy
import sys
sys.path.append('./src/scene')
from lights import set_ambient_light
from clear import clean_scene
from b_object import set_object
from cameras import create_camera




FRAMES = [75, 135, 200]

clean_scene()

create_camera()

set_object(FRAMES[0])

set_ambient_light()