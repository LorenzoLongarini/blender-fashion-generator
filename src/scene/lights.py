import bpy

def set_ambient_light():
    # Access the world settings to set ambient light
    world = bpy.context.scene.world
    world.use_nodes = True
    ambient_light = world.node_tree.nodes.new('ShaderNodeBackground')
    ambient_light.inputs['Strength'].default_value = 0.5  # Adjust the strength as needed