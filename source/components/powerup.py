__author__ = 'Team 10'

import pygame as pg
from .. import setup, tools
from .. import constants as c
from . import stuff

class Powerup(stuff.Stuff):
    def __init__(self, x, y, sheet, image_rect_list, scale):
        stuff.Stuff.__init__(self, x, y, sheet, image_rect_list, scale)
        self.rect.centerx = x 
        self.state = c.REVEAL
        self.y_vel = -1
        self.x_vel = 0
        self.direction = c.RIGHT
        self.box_height = y
        self.gravity = 1
        self.max_y_vel = 8
        self.animate_timer = 0
    
    def update_position(self, level):
        self.rect.x += self.x_vel
        self.check_x_collisions(level)
        
        self.rect.y += self.y_vel
        self.check_y_collisions(level)
        
        if self.rect.x <= 0:
            self.kill()
        elif self.rect.y > (level.viewport.bottom):
            self.kill()

    def check_x_collisions(self, level):
        sprite_group = pg.sprite.Group(level.ground_step_pipe_group,
                            level.brick_group, level.box_group)
        sprite = pg.sprite.spritecollideany(self, sprite_group)
        if sprite:
            if self.direction == c.RIGHT:
                self.rect.right = sprite.rect.left-1
                self.direction = c.LEFT
            elif self.direction == c.LEFT:
                self.rect.left = sprite.rect.right
                self.direction = c.RIGHT
            self.x_vel = self.speed if self.direction == c.RIGHT else -1 * self.speed
            if sprite.name == c.MAP_BRICK:
                self.x_vel = 0
    
    def check_y_collisions(self, level):
        sprite_group = pg.sprite.Group(level.ground_step_pipe_group,
                            level.brick_group, level.box_group)

        sprite = pg.sprite.spritecollideany(self, sprite_group)
        if sprite:
            self.y_vel = 0
            self.rect.bottom = sprite.rect.top
            self.state = c.SLIDE
        level.check_is_falling(self)

    def animation(self):
        self.image = self.frames[self.frame_index]

class Mushroom(Powerup):
    def __init__(self, x, y):
        Powerup.__init__(self, x, y, setup.GFX[c.ITEM_SHEET],
                [(0, 0, 16, 16)], c.SIZE_MULTIPLIER)
        self.type = c.TYPE_MUSHROOM
        self.speed = 2

    def update(self, game_info, level):
        if self.state == c.REVEAL:
            self.rect.y += self.y_vel
            if self.rect.bottom <= self.box_height:
                self.rect.bottom = self.box_height
                self.y_vel = 0
                self.state = c.SLIDE
        elif self.state == c.SLIDE:
            self.x_vel = self.speed if self.direction == c.RIGHT else -1 * self.speed
        elif self.state == c.FALL:
            if self.y_vel < self.max_y_vel:
                self.y_vel += self.gravity
        
        if self.state == c.SLIDE or self.state == c.FALL:
            self.update_position(level)
        self.animation()

class LifeMushroom(Mushroom):
    def __init__(self, x, y):
        Powerup.__init__(self, x, y, setup.GFX[c.ITEM_SHEET],
                [(16, 0, 16, 16)], c.SIZE_MULTIPLIER)
        self.type = c.TYPE_LIFEMUSHROOM
        self.speed = 2


