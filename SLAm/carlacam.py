# creating this to interface directly with CARLA without gym or scenic

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time

#constants
port = 2000
map = 'Town05'


def main():
    actor_list = []
    
    try:
        # create client that sends requests to simulator
        client = carla.Client('localhost', port)
        carla.set_timeout(2.0)
        
        # gets the world currently running and gets only the vehicle  blueprint_library
        client.load_world(map)
        world = client.get_world()
        bp_lib = world.get_blueprint_library()
        #choose a vehicle blueprint at random
        bp = random.choice(blueprint_library.filter('vehicle'))
        # bp.set_attribute('color', 'blue') #idek it's unnessary
        # set spawn point at random on map
        transform = random.choice(world.get_map().get_spawn_point())
        # spawns the car
        car = world.spawn_actor(bp, transform)
        
        # ensures the car wouldn't be destroyed untill the "destroy" call is made
        actor_list.append(car)
        print('created: ' + car.type_id)

        car.set_autopilot(True)

        # camera part
        # Create a transform to place the camera on top of the vehicle
        camera_init_trans = carla.Transform(carla.Location(z=1.5))
        # We create the camera through a blueprint that defines its properties
        camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
        # We spawn the camera and attach it to our ego vehicle
        camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)


        

        
