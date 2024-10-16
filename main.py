# main.py

import bpy
import sys
# Import functions from the required modules

sys.path.append('./src/scene')

from cameras import create_camera
from b_object import set_object
from lights import set_ambient_light
from clear import clean_scene


FRAMES = [75, 135, 200]

clean_scene()

create_camera()

set_object(FRAMES[0])

set_ambient_light()