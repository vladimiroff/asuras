from libs.vec2d import Vec2d
from libs.tmx import cells

class Obstacle:
    def __init__(self):
        self.pos = 0
        self.points = []
        self.pivot_points = []

def collision_check(entity, tilemap, direction):
        tile_container = (entity.rect.center[0] // tilemap.layers[0].tile_width, 
                          entity.rect.center[1] // tilemap.layers[0].tile_height)
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
        player.pos = entity.position + direction
        player.points = entity.points
        vehicle_colider = Detection(player, obstacles)
        vehicle_colider.line_by_line_check()

        entity.near_obstacles = obstacles

        return vehicle_colider

class Detection:
    '''
    Just some basic collision detection using
    Cartesian equation of a line
    '''

    def __init__(self, entity, objects):
        self.collisions = []
        self.collision_lines = []
        self.entity = entity
        self.objects = objects

    def line_by_line_check(self):
        self.collisions[:] = []
        self.collision_lines[:] = []
        previos_point = self.entity.points[-1]
        for collidable in self.objects:
            collidable_previous_point = collidable.points[-1]
            for point in self.entity.points:
                for collidable_point in collidable.points:
                    self.line_collider([self.entity.pos + previos_point,
                                      self.entity.pos + point],
                                     [collidable.pos + collidable_previous_point,
                                      collidable.pos + collidable_point])
                    collidable_previous_point = collidable_point
                previos_point = point

    def _line_check(self, line, crosspoint):
        if line[0][0] < line[1][0]:
            return line[0][0] < crosspoint and crosspoint < line[1][0]
        else:
            return line[0][0] > crosspoint and crosspoint > line[1][0]

    def line_collider(self, first_line, second_line):
        if first_line[1][0] == first_line[0][0] and second_line[1][0] == second_line[0][0]:
            return False
        elif first_line[1][0] == first_line[0][0]:
            if self.cartesian_equation(first_line, second_line):
                self.collision_lines.append(second_line)
                return True
            else:
                return False 
        elif second_line[1][0] == second_line[0][0]:
            if self.cartesian_equation(second_line, first_line):
                self.collision_lines.append(second_line)
                return True
            else:
                return False
        else:
            a_prime = (first_line[1][1]-first_line[0][1])/(first_line[1][0]-first_line[0][0])
            b_prime = first_line[0][1] - a_prime * first_line[0][0]
            a_second = (second_line[1][1]-second_line[0][1])/(second_line[1][0]-second_line[0][0])
            b_second = second_line[0][1] - a_second * second_line[0][0]

            if not a_prime == a_second:
                crosspoint = (b_second - b_prime)/(a_prime - a_second)
                if self._line_check(first_line, crosspoint) and self._line_check(second_line, crosspoint):
                    self.collisions.append(Vec2d(crosspoint, a_prime * crosspoint + b_prime))
                    self.collision_lines.append(second_line)
                    return True
            return False

    def cartesian_equation(self, first_line, second_line):
        a_second = (second_line[1][1]-second_line[0][1])/(second_line[1][0]-second_line[0][0])
        b_second = second_line[0][1] - a_second * second_line[0][0]

        crosspoint = a_second * first_line[0][0] + b_second
        if first_line[0][1] < first_line[1][1]:
            if first_line[0][1] < crosspoint and crosspoint < first_line[1][1]:
                if self._line_check(second_line, first_line[0][0]):
                    self.collisions.append(Vec2d(first_line[0][0], crosspoint))
                    return True
            return False
        else:
            if first_line[0][1] > crosspoint and crosspoint > first_line[1][1]:
                if self._line_check(second_line, first_line[0][0]):
                    self.collisions.append(Vec2d(first_line[0][0], crosspoint))
                    return True
            return False
