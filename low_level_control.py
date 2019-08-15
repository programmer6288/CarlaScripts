#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys
from json_converter import JsonData
import math

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import logging
import random

try:
    import pygame
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

try:
    import queue
except ImportError:
    import Queue as queue


def draw_image(surface, image):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    surface.blit(image_surface, (0, 0))


def get_font():
    fonts = [x for x in pygame.font.get_fonts()]
    default_font = 'ubuntumono'
    font = default_font if default_font in fonts else fonts[0]
    font = pygame.font.match_font(font)
    return pygame.font.Font(font, 14)


def should_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return True
    return False

def main():
    is_in_init = True
    json_converter = JsonData('interesting_lane_change.txt')
    actor_list = []
    waypoint_list, heading_list, throttle_list, t_step, _ = json_converter.get_path_information()
    print(throttle_list)
    i=0
    k=0
    frame_limit = t_step*30
    pygame.init()

    display = pygame.display.set_mode(
        (800, 600),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    font = get_font()
    clock = pygame.time.Clock()

    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    try:
        #m = world.get_map()
        start_pose = carla.Transform(carla.Location(x=-295.5, y=30.1575, z=2.12094))
        #waypoint = m.get_waypoint(start_pose.location)

        blueprint_library = world.get_blueprint_library()

        vehicle = world.spawn_actor(
            random.choice(blueprint_library.filter('vehicle.chevrolet.impala')),
            start_pose)
        actor_list.append(vehicle)
        #vehicle.set_simulate_physics(False)

        camera = world.spawn_actor(
            blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=vehicle)
        actor_list.append(camera)

        # Make sync queue for sensor data.
        image_queue = queue.Queue()
        camera.listen(image_queue.put)

        frame = None

        display = pygame.display.set_mode(
            (800, 600),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        font = get_font()

        clock = pygame.time.Clock()

	

        while True:
            if should_quit():
                return

            clock.tick()
            world.tick()
            ts = world.wait_for_tick()

            '''if frame is not None:
                if ts.frame_count != frame + 1:
                    logging.warning('frame skip!')'''

            frame = ts.frame_count

            while True:
                image = image_queue.get()
		if is_in_init and vehicle.get_velocity().x<5:
			vehicle.apply_control(carla.VehicleControl(throttle=1.0))
		elif throttle_list[i]>0:
			vehicle.apply_control(carla.VehicleControl(throttle=throttle_list[i]/4, steer=heading_list[i]*2/math.pi))
		else:
			vehicle.apply_control(carla.VehicleControl(brake=-1*throttle_list[i]/4, steer=heading_list[i]*2/math.pi))
		k+=1
	
                if k==frame_limit:
		    i+=1
                    k=0
	            print vehicle.get_velocity().x
                if image.frame_number == ts.frame_count:
                    break
                '''logging.warning(
                    'wrong image time-stampstamp: frame=%d, image.frame=%d',
                    ts.frame_count,
                    image.frame_number)'''

            #waypoint = random.choice(waypoint.next(2))
            #vehicle.set_transform(waypoint.transform)

            draw_image(display, image)

            text_surface = font.render('% 5d FPS' % clock.get_fps(), True, (255, 255, 255))
            display.blit(text_surface, (8, 10))

            pygame.display.flip()

    finally:

        print('destroying actors.')
        for actor in actor_list:
            actor.destroy()

        pygame.quit()
        print('done.')


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
