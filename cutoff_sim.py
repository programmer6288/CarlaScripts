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
import os
import random
import time


def main():
    actor_list = []
    vehicle_list = []

    try:
	        
	client = carla.Client('localhost', 2000)
        client.set_timeout(10)

        
        world = client.get_world()

	settings = world.get_settings()
	settings.fixed_delta_seconds = 0.05
	world.apply_settings(settings)
	
	blueprint_library = world.get_blueprint_library()
	
	bp = blueprint_library.find('vehicle.bmw.grandtourer')
	
	transform = carla.Transform(carla.Location(x=-240, y=30.1575, z=10))


	
	ego_vehicle = world.spawn_actor(bp, transform)

	actor_list.append(ego_vehicle)
	vehicle_list.append(ego_vehicle)

	
	
	transform = carla.Transform(carla.Location(x=-240, y=26.4518, z=10))

	jerk_vehicle = world.spawn_actor(bp, transform)

	actor_list.append(jerk_vehicle)
	vehicle_list.append(jerk_vehicle)

	transform = carla.Transform(carla.Location(x=-240, y=33.8632, z=10))
	
	side_vehicle = world.spawn_actor(bp, transform)

	actor_list.append(side_vehicle)
	vehicle_list.append(side_vehicle)

	transform = carla.Transform(carla.Location(x=-230, y=30.1575, z=10))	

	front_vehicle = world.spawn_actor(bp, transform)

	actor_list.append(front_vehicle)
	vehicle_list.append(front_vehicle)

	
	

	for vehicle in vehicle_list:
		vehicle.set_autopilot(True)

	time.sleep(35)

	front_vehicle.set_autopilot(False)
	jerk_vehicle.set_autopilot(False)
	side_vehicle.set_autopilot(False)

	front_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
	jerk_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
	side_vehicle.apply_control(carla.VehicleControl(throttle=0.5))

	time.sleep(4)

	front_vehicle.apply_control(carla.VehicleControl(throttle=1.0))
	jerk_vehicle.apply_control(carla.VehicleControl(throttle=1.0))
	side_vehicle.apply_control(carla.VehicleControl(throttle=1.0))

	
		
	jerk_vehicle.set_autopilot(False)

	jerk_vehicle.apply_control(carla.VehicleControl(throttle=1.0))
	
	time.sleep(5)
	
	front_vehicle.set_autopilot(False)
	
	front_vehicle.apply_control(carla.VehicleControl(throttle=1.0))
	
	time.sleep(0.7)

	front_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
	
	jerk_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=1.0))

	time.sleep(0.4)

	jerk_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=-1.0))

	time.sleep(0.6)

	jerk_vehicle.apply_control(carla.VehicleControl(throttle=0.5))

	front_vehicle.apply_control(carla.VehicleControl(brake=0.0))
	
	time.sleep(1)

	jerk_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=1.0))

	time.sleep(1)

	jerk_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=-1.0))

	time.sleep(1)
	

	time.sleep(100)

	
	
		

    finally:

        print('destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    main()
