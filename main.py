import bpy
import sys
sys.path.append('..src/utils')
from clear import clean_scene

# bpy.ops.scene.delete()
# bpy.ops.scene.new(type="NEW")

clean_scene()
path = 'D:/DeepFashion/1-1/model_cleaned.obj'
imported_object = bpy.ops.wm.obj_import(filepath=path)
obj_object = bpy.context.selected_objects[0]
print('Imported name: ', obj_object.name)
