import bpy
from math.utils import Vector

def point_camera_at(camera_obj, target):
    """
    Rotates the camera object to point towards the target (a Vector).
    """
    direction = target - camera_obj.location
    # Invert the direction for Blender's coordinate system
    rotation = direction.to_track_quat('Z', 'Y').to_euler()
    camera_obj.rotation_euler = rotation

def calculate_optimal_focal_length(camera_obj, target_obj, margin=1.2):
    """
    Adjusts the camera's focal length so that the target object is fully visible in the camera's view.
    `margin` is a multiplier to add some padding around the object.
    """
    # Get the camera's position
    cam_location = camera_obj.location
    # Get the bounding box of the object (in world coordinates)
    bbox_corners = [target_obj.matrix_world @ Vector(corner) for corner in target_obj.bound_box]

    # Calculate the bounding box center and its size (largest distance between any two corners)
    bbox_center = sum(bbox_corners, Vector()) / 8
    max_dist = max((bbox_corner - bbox_center).length for bbox_corner in bbox_corners)

    # Calculate the distance from the camera to the object center
    cam_to_bbox_center_dist = (cam_location - bbox_center).length

    # Adjust the camera's focal length based on the distance and size of the bounding box
    # We use a basic field of view formula here: focal_length = distance / size * constant
    focal_length = (cam_to_bbox_center_dist / (max_dist * margin)) * 35  # The 35 is a "base" focal length
    camera_obj.data.lens = focal_length

def create_camera(target_obj):
    scn = bpy.context.scene
    target = target_obj.location  # Use the object's location as the target point

    # create the first camera
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 18

    # create the first camera object
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    cam_obj1.location = (3.0, -4.0, 2.0)  # Set the first camera's location
    scn.collection.objects.link(cam_obj1)

    # Make the first camera point to the center
    point_camera_at(cam_obj1, target)

    # Adjust the camera's zoom (focal length) dynamically to fit the object
    calculate_optimal_focal_length(cam_obj1, target_obj)

    # create the second camera
    cam2 = bpy.data.cameras.new("Camera 2")
    cam2.lens = 18

    # create the second camera object
    cam_obj2 = bpy.data.objects.new("Camera 2", cam2)
    cam_obj2.location = (-3.0, 4.0, 2.0)  # Set the second camera's location
    scn.collection.objects.link(cam_obj2)

    # Make the second camera point to the center
    point_camera_at(cam_obj2, target)

    # Adjust the second camera's zoom (focal length) dynamically to fit the object
    calculate_optimal_focal_length(cam_obj2, target_obj)


# Example usage:
target_obj = bpy.context.active_object  # You can replace this with any object in your scene
create_camera(target_obj)