import bpy
import sys
sys.path.append('..src/utils')
from clear import clean_scene
from import_obj import import_obj
from add_texture import add_texture

clean_scene()

import_obj()

add_texture()


