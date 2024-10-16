import bpy

def set_lights():
    # world = bpy.context.scene.world
    # world.use_nodes = True
    # ambient_light = world.node_tree.nodes.new('ShaderNodeBackground')
    # ambient_light.inputs['Strength'].default_value = 0.5
    world = bpy.data.worlds['World']

    # Assicurati che il mondo usi i nodi
    world.use_nodes = True
    node_tree = world.node_tree

    # Rimuovi tutti i nodi esistenti
    node_tree.nodes.clear()

    # Aggiungi il nodo Background
    background_node = node_tree.nodes.new(type="ShaderNodeBackground")
    # background_node.inputs[0].default_value = (0.05, 0.2, 0.6, 1)  # Imposta un colore bluastro, RGBA
    background_node.inputs[0].default_value = (1.0, 1.0, 1.0, 1) # bianco
    background_node.inputs[1].default_value = 1.0  # Imposta l'intensità della luce ambientale

    # Aggiungi il nodo World Output
    world_output = node_tree.nodes.new(type="ShaderNodeOutputWorld")

    # Collega il nodo Background all'Output del mondo
    node_tree.links.new(background_node.outputs[0], world_output.inputs[0])

    # Imposta il motore di rendering (Cycles o Eevee)
    bpy.context.scene.render.engine = 'CYCLES'  # O 'BLENDER_EEVEE'


#     bpy.ops.object.light_add(type='AREA')
#     light_ob = bpy.context.object
#     light = light_ob.data
#     light.energy = 500
#     light.color = (1, 0, 0)

# import bpy
# def set_lights():
#     # world = bpy.data.worlds["World"]
#     bpy.data.scenes['Scene'].render.engine = 'CYCLES'
#     world = bpy.data.worlds['World']
#     world.use_nodes = True

#     # changing these values does affect the render.
#     bg = world.node_tree.nodes['Background']
#     bg.inputs[0].default_value[:3] = (0.5, .1, 0.6)
#     bg.inputs[1].default_value = 1.0

#     bpy.ops.render.render()

    # faux_name = "tensor_" + str(time.time()) + ".png"
    # fp = os.path.join("/home/zeffii/Desktop", faux_name)
    # bpy.data.images['Render Result'].save_render(filepath=fp)