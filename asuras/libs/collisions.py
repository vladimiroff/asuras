from libs.vec2d import Vec2d

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
