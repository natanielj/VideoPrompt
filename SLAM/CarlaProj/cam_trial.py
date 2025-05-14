import glob
import os
import sys
import time
import carla
import shutil

port = 2000 #default port
out_dir = "./cam_out"

# clear output directory
def clean_cam_out(out_dir):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    print(f"Cleaned up and prepared output directory: {out_dir}")

def main():
    #connect to carla client
    client = carla.Client("localhost", port)
    client.set_timeout(10.0)

    #load world and get the world's blueprint library
    world = client.get_world()
    bp_lib = world.get_blueprint_library()
    
    # setup spectator view
    spec = world.get_spectator()
    cam_loc = carla.Location(x=110.03, y=216.0, z=50.0)
    cam_rot = carla.Rotation(pitch=-69.0, yaw=0.0, roll=0.0)
    cam_trans = carla.Transform(cam_loc, cam_rot)

    spec.set_transform(cam_trans)

    #setup car 
    car_bp = bp_lib.find("vehicle.chevrolet.impala")
    spawn_points = world.get_map().get_spawn_points()
    car_spawn_point = spawn_points[4]
    
    vehicle = world.spawn_actor(car_bp, car_spawn_point)
    print("Vehicle spawned")

    vehicle_extent = vehicle.bounding_box.extent
    vehicle_length = vehicle_extent.x * 2
    vehicle_width = vehicle_extent.y * 2
    vehicle_height = vehicle_extent.z * 2
    
    print(f"Vehicle dimensions - Length: {vehicle_length} m, Width: {vehicle_width} m, Height: {vehicle_height} m")
        
    vehicle.set_autopilot(True)
    # Find a camera blueprint
    camera_bp = bp_lib.find('sensor.camera.rgb')

    # Adjust camera attributes (optional)
    camera_bp.set_attribute('image_size_x', '1920')
    camera_bp.set_attribute('image_size_y', '1080')
    camera_bp.set_attribute('fov', '105') # Field of view in degrees
    camera_bp.set_attribute('sensor_tick', '1.0') # Capture image every second

    # Calculate camera location based on vehicle dimensions
    camera_location = carla.Location(
        x=vehicle_extent.x + 0.5,    # Slightly forward from the vehicle's front
        y=0.0,                       # Centered horizontally on the vehicle
        z=vehicle_extent.z           # Elevated above the roof
    )

    # Adjust camera rotation to face forward
    camera_rotation = carla.Rotation(pitch=-10.0, yaw=0.0, roll=0.0)  # Tilt slightly downward
    camera_transform = carla.Transform(camera_location, camera_rotation)
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

        # Print the current working directory (where files will be saved)
    print("Saving files to:", os.getcwd())

    print("Available Spawn Points:")
    for idx, spawn_point in enumerate(spawn_points):
        print(f"Spawn Point {idx}: Location({spawn_point.location.x}, {spawn_point.location.y}, {spawn_point.location.z}), "
              f"Rotation({spawn_point.rotation.pitch}, {spawn_point.rotation.yaw}, {spawn_point.rotation.roll})")


    # Create directory for saving images if it doesn't exist
    clean_cam_out(out_dir)

    camera.listen(lambda image: image.save_to_disk(f'{out_dir}/{image.frame}.png'))
     
    try:
        # Let the simulation run for 30 seconds
        time.sleep(30)
    
    finally:
        # Clean up by destroying actors
        camera.stop()
        camera.destroy()
        vehicle.destroy()
        print("Actors destroyed, simulation finished.") 
if __name__ == "__main__":
    main()
