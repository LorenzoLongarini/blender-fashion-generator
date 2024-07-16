import bpy
import os
import math

# Percorso al dataset DeepFashion3D (cartella con i modelli mesh)
deepfashion3d_path = "/Users/alerong/Downloads/Computer Graphics/Dataset/filtered_registered_mesh-001"

# Percorso di output per i dataset generati
output_path = "/Users/alerong/Downloads/Computer Graphics/output"

# Numero di variazioni nel numero di immagini renderizzate
variations = [75, 135, 200]

def parse_obj(file_path):
    """
    Funzione per parsare un file OBJ e restituire i vertici e le facce.
    """
    vertices = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.split()
                vertex = (float(parts[1]), float(parts[2]), float(parts[3]))
                vertices.append(vertex)
            elif line.startswith('f '):
                parts = line.split()
                face = []
                for part in parts[1:]:
                    vertex_index = part.split('/')[0]
                    face.append(int(vertex_index) - 1)
                faces.append(tuple(face))

    return vertices, faces

def import_model_with_texture(obj_path):
    """
    Funzione per importare un modello 3D da un file OBJ.
    """
    vertices, faces = parse_obj(obj_path)

    # Crea una nuova mesh e oggetto in Blender
    mesh = bpy.data.meshes.new("ImportedMesh")
    obj = bpy.data.objects.new("ImportedObject", mesh)
    bpy.context.collection.objects.link(obj)

    # Crea la mesh in Blender
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # Centra l'oggetto nella scena e lo orienta verticalmente
    obj.location = (0, 0, 0)
    obj.rotation_euler = (math.radians(90), 0, 0)  # Orienta l'oggetto verticalmente
    
    # Ridimensiona l'oggetto se necessario
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.scale_clear(clear_delta=False)
    
    return obj

def setup_and_render(output_dir, num_images, model):
    """
    Funzione per impostare la scena e renderizzare le immagini.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Impostazioni della scena, telecamera e luci
    # Rimuovi la telecamera e la luce esistenti
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # Aggiungi luci per migliorare l'illuminazione da diverse prospettive
    light_locations = [
        (0, 0, 5), (5, 5, 5), (-5, -5, 5), (5, -5, 5), (-5, 5, 5),
        (0, 0, -5), (-5, 5, -5), (5, -5, -5), (5, 5, -5), (-5, -5, -5)
    ]
    for loc in light_locations:
        bpy.ops.object.light_add(type='POINT', location=loc)
        light = bpy.context.object
        light.data.energy = 1000  # Luce più soft per ridurre le ombre dure

    # Posizione e rotazione della camera
    camera_distance = 2  # Distanza della telecamera dal centro
    cam_pos = (camera_distance, 0, 1.5)
    cam_rot = (math.radians(0), 0, math.radians(90))

    # Aggiungi una nuova telecamera
    bpy.ops.object.camera_add(location=cam_pos)
    cam = bpy.context.selected_objects[0]
    cam.rotation_euler = cam_rot
    bpy.context.scene.camera = cam

    # Aggiungi un vincolo Track To alla telecamera per puntare verso il centro della scena (0, 0, 0)
    track_to = cam.constraints.new(type='TRACK_TO')
    empty_obj = bpy.data.objects.new("Empty", None)
    bpy.context.collection.objects.link(empty_obj)
    empty_obj.location = (0, 0, 0)
    track_to.target = empty_obj
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

    # Configura le impostazioni di rendering
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128  # Aumenta i campioni per una qualità migliore
    bpy.context.scene.cycles.use_denoising = True  # Abilita il denoising
    bpy.context.scene.render.resolution_x = 3840  # Risoluzione 4K
    bpy.context.scene.render.resolution_y = 2160

    # Renderizzazione delle immagini
    for i in range(num_images):
        # Ruota il modello ogni 90 gradi
        model.rotation_euler[2] += math.radians(360 / num_images)

        # Renderizza l'immagine
        bpy.context.scene.render.filepath = os.path.join(output_dir, f"image_{i:03d}.png")
        bpy.ops.render.render(write_still=True)

    # Rimuovi la telecamera e l'oggetto vuoto dopo il rendering
    bpy.ops.object.delete()
    bpy.data.objects.remove(empty_obj)

# Loop attraverso le sottocartelle di DeepFashion3D
for subdir, dirs, files in os.walk(deepfashion3d_path):
    obj_file = None
    texture_file = None

    for file in files:
        if file.endswith(".obj"):
            obj_file = os.path.join(subdir, file)
        elif file.endswith(".png"):
            texture_file = os.path.join(subdir, file)

    if obj_file:
        # Importa e centra il modello
        model = import_model_with_texture(obj_file)

        # Loop attraverso le variazioni
        for num_images in variations:
            category = os.path.basename(subdir)
            output_dir = os.path.join(output_path, category, f"{num_images}_images")
            setup_and_render(output_dir, num_images, model)
    
    # Pulizia della scena per il prossimo modello
    bpy.ops.wm.read_factory_settings(use_empty=True)