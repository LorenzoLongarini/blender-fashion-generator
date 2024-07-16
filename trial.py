import bpy
import random
import math


def purge_orphans():
    if bpy.app.version >= (3, 0, 0):
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
    else:
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene
    """
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # # in the case when you modify the world shader
    # world_names = [world.name for world in bpy.data.worlds]
    # for name in world_names:
    #     bpy.data.worlds.remove(bpy.data.worlds[name])
    # # create a new world data block
    # bpy.ops.world.new()
    # bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


#bpy.ops.scene.delete()
#bpy.ops.scene.new(type=‘NEW’)

#path = 'D:/DeepFashion/1-1/model_cleaned.obj'
#imported_object = bpy.ops.wm.obj_import(filepath=path)
#obj_object = bpy.context.selected_objects[0]
#print('Imported name: ', obj_object.name)

# def main():
#     return

# if 