import math
from pygame import sprite, transform, image
from libs.collisions import Detection, Obstacle
from libs.tmx import cells
from libs.vec2d import Vec2d

class Bullet(sprite.Sprite):

    speed = 15
    direction = Vec2d(0, 0)
    rotation = 0
    position = Vec2d(0, 0)
    points = [Vec2d(2, -speed), Vec2d(2, speed)]
    kill_in_the_next_frame = False
    life = 200
    

    def __init__(self, position, direction, type, *sprite_groups):
        super().__init__(*sprite_groups)
        self.direction = direction
        direction.length = 1
        if direction[1] < 0:
            modify = (90 - math.degrees(math.asin(direction[0]))) * 2
        else:
            modify = 0
        self.rotation = math.degrees(math.asin(direction[0])) + modify
        self.position = position

        for point in self.points:
            point.rotate(360 - self.rotation)

        base_image = image.load('resources/bomb.png')
        self.image = transform.rotate(base_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def collision_check(self, tilemap, direction):
        tile_container = (self.rect.center[0] // tilemap.layers[0].tile_width, 
                          self.rect.center[1] // tilemap.layers[0].tile_height)
        obstacles = []
        for line in range(3):
            for col in range(3):
                curent_tile = tilemap.layers[1][(tile_container[0] + line - 1,
                                                 tile_container[1] + col - 1)]
                if type(curent_tile) is cells.Cell:
                    if curent_tile.tile.properties['collidable']:
                        new_collidable_object = Obstacle()
                        new_collidable_object.pos = Vec2d(curent_tile.topleft)
                        new_collidable_object.points = []
                        if not curent_tile.tile.properties['points']:
                            new_collidable_object.points.append(Vec2d(0, 0))
                            new_collidable_object.points.append(Vec2d(101, 0))
                            new_collidable_object.points.append(Vec2d(101, 101))
                            new_collidable_object.points.append(Vec2d(0, 101))
                        else:
                            object_points = curent_tile.tile.properties['points'].split(';')
                            for point in object_points:
                                point_coords = point.split(',')
                                new_collidable_object.points.append(Vec2d(int(point_coords[0]),
                                                                          int(point_coords[1])))
                        obstacles.append(new_collidable_object)

        player = Obstacle()
        player.pos = self.position + direction
        player.points = self.points
        vehicle_colider = Detection(player, obstacles)
        vehicle_colider.line_by_line_check()

        self.near_obstacles = obstacles

        return vehicle_colider

    def update(self, pressed, time_delta, tilemap):
        if self.kill_in_the_next_frame or not self.life:
            print("I die!")
            self.kill()
        self.direction.length = self.speed
        self.position += self.direction
        self.rect.center = self.position
        self.life -= 1
        predicted_collision_result = self.collision_check(tilemap, self.direction)
        if predicted_collision_result.collisions:
            self.rect.center = predicted_collision_result.collisions[0]
            self.kill_in_the_next_frame = True
