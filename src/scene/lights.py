import bpy
from mathutils import Vector

def set_lights():
    # Configurazione del mondo e dello sfondo
    world = bpy.data.worlds['World']
    world.use_nodes = True
    node_tree = world.node_tree
    node_tree.nodes.clear()

    background_node = node_tree.nodes.new(type="ShaderNodeBackground")
    background_node.inputs[0].default_value = (1.0, 1.0, 1.0, 1)  # Colore bianco
    background_node.inputs[1].default_value = 1.0  # Intensità della luce ambientale

    world_output = node_tree.nodes.new(type="ShaderNodeOutputWorld")
    node_tree.links.new(background_node.outputs[0], world_output.inputs[0])

    bpy.context.scene.render.engine = 'CYCLES'  # Imposta il motore di rendering su 'CYCLES'

    # Aggiunta di una luce Sun al centro della scena
    bpy.ops.object.light_add(type='SUN')  # Aggiunge una luce di tipo Sun
    luce = bpy.context.object
    luce.name = "Luce_Solare"
    luce.location = (0, 0, 0)  # Posiziona la luce sopra la scena, allineata all'asse Z
    luce.data.energy = 5  # Intensità della luce (modifica se necessario)

    # Ottieni l'oggetto importato dinamicamente
    imported_objects = [obj for obj in bpy.context.scene.objects if obj.select_get()]
    if imported_objects:
        oggetto = imported_objects[0]  # Usa il primo oggetto selezionato
        print(f"Oggetto selezionato: {oggetto.name}")

        # Posiziona la luce sopra l'oggetto
        luce.location = (oggetto.location.x, oggetto.location.y, 10)

        # Calcola la direzione dalla luce all'oggetto
        direzione = oggetto.location - luce.location
        direzione.normalize()

        # Imposta la rotazione della luce verso l'oggetto
        luce.rotation_euler = direzione.to_track_quat('Z', 'Y').to_euler()
    else:
        print("Nessun oggetto selezionato nella scena!")

# Chiama la funzione per impostare le luci
set_lights()