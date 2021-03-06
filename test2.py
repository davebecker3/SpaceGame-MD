#
# cocos2d
# http://python.cocos2d.org
#

from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import random
import math

import pyglet
from pyglet.window import key
from pyglet.gl import *

import cocos
from cocos.director import director
import cocos.collision_model as cm
import cocos.euclid as eu
# import cocos.actions as ac

from cocos import actions, layer, sprite, scene

class HelloWorld(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)
        # self.add_sprite()

    def add_sprite(self):
        heroimage = pyglet.resource.image('hero.png')
        player = cocos.sprite.Sprite(heroimage)
        player.position = (100, 100)
        self.add(player)


#class for movement of main character
class HeroShipMovement(actions.Move):
    def step(self, dt):
        super(HeroShipMovement, self).step(dt)
        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 200 * (keyboard[key.UP] - keyboard[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)


        #move = self.target.position
        #for move in range(0, 400):
           # move = move + 25
           # self.target.position = move;

class HeroShipMovement2(actions.Move):
    def step(self, dt):
        super(HeroShipMovement2, self).step(dt)
        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 200 * (keyboard[key.UP] - keyboard[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)
        #self.add(self.msg_pos_x)



class HeroShip(cocos.sprite.Sprite):
    def __init__(self, image):
        super(HeroShip, self).__init__(image)
        self.image = image
        self.position = (100, 100)
        self.velocity = (0,0)
        self.cshape = cm.AARectShape(eu.Vector2(self.position), 32, 32)

class TestSprite(cocos.sprite.Sprite):
    def __init__(self, image):
        super(TestSprite, self).__init__(image)
        self.image = image
        self.position = (100, 100)
        self.velocity = (0,0)
        self.cshape = cm.AARectShape(eu.Vector2(self.position), 32, 32)
        shipPosition = self.target.position
        self.msg_counter = cocos.text.Label(str(shipPosition),
                            font_name='Times New Roman',
                            font_size=32,
                            anchor_x='center', anchor_y='center')

        self.msg_counter.position = (120, 240)
        self.add(self.msg_counter)


class Asteroid(cocos.sprite.Sprite):
    def __init__(self, image, position):
        super(Asteroid, self).__init__(image)
        self.image = image
        self.position = position
        self.velocity = (0,0)
        self.cshape = cm.CircleShape(eu.Vector2(self.position), 16)
        self.type = 'asteroid'


class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        # self.CollMan = cm.CollisionManager()
        #self.CollMan = cm.CollisionManagerGrid(0.0, 640,
                                               #0.0, 480,
                                                   # 100,
                                                    #100)
        self.CollMan = cm.CollisionManagerBruteForce()
        self.add_hero()
        self.add_asteroids()
        self.add_asteroid()
        #self.boom()
        # self.add_boss()
        self.CollMan.add(self.hero)
        self.CollMan.add(self.asteroid1)
        self.CollMan.add(self.asteroid2)

        #self.check_known
        # self.check_list()

        # iterator for "count" method test.
        self.i = 0

        #proximity to check distance between hero & test asteroid.
        self.proximity = (0.0, 0.0)

        self.asteroid_list = set()
        self.remove_asteroid_list = set()
        self.asteroid_list.add(self.asteroid_x)
        self.asteroid_list.add(self.asteroid1)
        self.asteroid_list.add(self.asteroid2)


        # self.counter(self.i)
        self.add_count_label()
        self.add_pos_x_label()
        self.add_proximity_label()

        self.schedule(self.update)

    def displayX(self):
         self.msg_pos_x = cocos.text.Label(str(self.hero.position),
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
         self.msg_pos_x.position = (25, 25)
         self.add(self.msg_pos_x)




    def add_hero(self):
        heroImage = pyglet.resource.image('hero.png')
        # hero = cocos.sprite.Sprite(heroImage)
        self.hero = HeroShip(heroImage)
        # hero.position = (150, 150)
        #self.hero.do(HeroShipMovement())
        self.hero.do(HeroShipMovement2())
        self.add(self.hero)

    def add_boss(self):
        bossImage = pyglet.resource.image('boss.png')
        boss = cocos.sprite.Sprite(bossImage)
        boss.position = (300, 200)
        self.add(boss)

    def add_asteroids(self):
        aster1Image = pyglet.resource.image('asteroid.png')
        aster1Position = (150, 550)
        aster1Velocity = (0, 1000)

        aster2Image = pyglet.resource.image('asteroid_2.png')
        aster2Position = (200, 500)
        aster2Velocity = (100, 25)

        self.asteroid1 = Asteroid(aster1Image, aster1Position)
        self.asteroid2 = Asteroid(aster2Image, aster2Position)
        # boss.position = (300, 200)
        self.add(self.asteroid1)
        self.add(self.asteroid2)

        self.asteroid1.do(actions.MoveBy( (0, -600), 4) )
        self.asteroid2.do(actions.MoveBy( (100, -600), 8) )

    def add_asteroid(self):
        aster1Image = pyglet.resource.image('asteroid.png')
        aster1Position = (320, 240)
        aster1Velocity = (0, 0)
        self.asteroid_x = Asteroid(aster1Image, aster1Position)
        self.add(self.asteroid_x)

    def boom(self):
        self.msg_boom = cocos.text.Label('BOOM!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')

        self.msg_boom.position = 320, 440
        self.add(self.msg_boom)

    def add_count_label(self):
        self.msg_counter = cocos.text.Label("TEST",
                                 font_name='Times New Roman',
                                 font_size=16,
                                 anchor_x='center', anchor_y='center')

        self.msg_counter.position = (50, 450)
        self.add(self.msg_counter)

    def add_pos_x_label(self):
        self.msg_pos_x = cocos.text.Label("TEST",
                                 font_name='Times New Roman',
                                 font_size=16,
                                 anchor_x='center', anchor_y='center')

        self.msg_pos_x.position = (200, 25)
        self.add(self.msg_pos_x)

    def add_proximity_label(self):
        self.msg_proximity = cocos.text.Label("TEST",
                                 font_name='Times New Roman',
                                 font_size=16,
                                 anchor_x='center', anchor_y='center')

        self.msg_proximity.position = (400, 50)
        self.add(self.msg_proximity)

    def update_count_label(self, count_in):
        count = count_in
        self.msg_counter.element.text = (str(count))

    def update_pos_x_label(self):
        self.msg_pos_x.element.text = (str(self.hero.position))

    def update_proximity_label(self):
        # self.msg_proximity.element.text = (str(self.asteroid_x.position))
        self.msg_proximity.element.text = (str(self.proximity))

    def counter(self, count_in):
        count = count_in
        self.msg_counter = cocos.text.Label('Count = ' + str(count),
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        msg_x = 120
        # self.msg_counter.position = ((120 + count), 240 + count)
        self.msg_counter.position = (120, 240)
        self.add(self.msg_counter)

        # if (count % 1000 == 0):
        #     self.remove(self.msg_counter)

        #self.remove(self.msg_counter)


    def check_list(self):
        count_list = 0
        for item in self.CollMan.known_objs():
            count_list = (self.count +1)
        self.msg_count_list = cocos.text.Label('Count from list = ' + str(count_list),
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')

        self.msg_boom.position = 320, 440
        self.add(self.msg_count_list)

    def check_collision(self):
        for other in self.CollMan.iter_colliding(self.hero):
            actor_type = other.type
            if actor_type == 'asteroid':
                self.boom()

    def check_known(self):
        if self.CollMan.knows(self.hero):
            self.boom()

    def check_proximity(self):
        for asteroid in self.asteroid_list:
            self.proximity = (abs(asteroid.position[0] - self.hero.position[0]),
                              abs(asteroid.position[1] - self.hero.position[1]))
            # if ((self.hero.position[0] > 500.0 )and (self.hero.position[1] > 500.0)):
            if ((self.proximity[0] < 25.0 ) and (self.proximity[1] < 25.0)):
                self.boom()

    def remove_asteroid(self):
        for asteroid in self.asteroid_list:
            if (asteroid.position[1] < 0):
                self.remove_asteroid_list.add(asteroid)

        for removable_asteroid in self.remove_asteroid_list:
            self.asteroid_list.remove(removable_asteroid)
            self.remove(removable_asteroid)
        self.remove_asteroid_list.clear()


    # def update(self, dt):
    def update(self, dt):
        pass
        # self.CollMan.clear()
        # self.CollMan.add(self.hero)
        # self.CollMan.add(self.asteroid1)
        # self.CollMan.add(self.asteroid2)
        # self.check_known()
        # self.check_collision()
        # self.displayX()

        # self.counter(self.i)
        self.i = (self.i + 1)

        # self.msg_counter.count = self.i
        # self.counter(self.i)
        self.update_count_label(self.i)
        self.update_pos_x_label()
        self.check_proximity()
        self.update_proximity_label()
        self.remove_asteroid()
        # if (self.i > 1000):
        #     self.remove(self.msg_counter)

if __name__ == "__main__":

    global keyboard

    # director init takes the same arguments as pyglet.window
    # cocos.director.director.init()
    director.init(width=640, height=480, autoscale=True, resizable = True)

    #initializing pyglet, which allows for keyboard import for character movement
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    # We create a new layer, an instance of HelloWorld
    hello_layer = HelloWorld()
    game_layer = GameLayer()

    # A scene that contains the layer hello_layer
    # main_scene = cocos.scene.Scene(hello_layer, game_layer)
    main_scene = cocos.scene.Scene(game_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )
