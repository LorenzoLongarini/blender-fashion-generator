import bpy
def import_obj():
    path = 'D:/DeepFashion/1-1/model_cleaned.obj'
    imported_object = bpy.ops.wm.obj_import(filepath=path)
    obj_object = bpy.context.selected_objects[0]
    print('Imported name: ', obj_object.name)