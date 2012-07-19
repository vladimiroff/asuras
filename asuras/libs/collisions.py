from libs.vec2d import Vec2d

class VectorDetection:
    ''' Just some basic collision detection using vectors '''

    def __init__(self):
        self.collisions = []
        entity = self.entity[0]
        previos_point = entity.points[-1]
        for collidable in self.items:
            collidable_previous_point = entity.points[-1]
            for point in entity.points:
                for collidable_point in collidable.points:
                    self.line_collider([entity.pos + previos_point,
                                      entity.pos + point],
                                     [collidable.pos + collidable_previous_point,
                                      collidable.pos + collidable_point])
                    collidable_previous_point = collidable_point
                previos_point = point

    def line_check(self, line, crosspoint):
        if line[0][0] < line[1][0]:
            return line[0][0] < crosspoint and crosspoint < line[1][0]
        else:
            return line[0][0] > crosspoint and crosspoint > line[1][0]

    def line_collider(self, first_line, second_line):
        def deckard_equation(first_line, second_line):
            a_second = (second_line[1][1]-second_line[0][1])/(second_line[1][0]-second_line[0][0])
            b_second = second_line[0][1] - a_second * second_line[0][0]

            crosspoint = a_second * first_line[0][0] + b_second
            if first_line[0][1] < first_line[1][1]:
                if first_line[0][1] < crosspoint and crosspoint < first_line[1][1]:
                    if self.line_check(second_line, first_line[0][0]):
                        self.collisions.append(Vec2d(first_line[0][0], crosspoint))
                        return True
                return False
            else:
                if first_line[0][1] > crosspoint and crosspoint > first_line[1][1]:
                    if self.line_check(second_line, first_line[0][0]):
                        self.collisions.append(Vec2d(first_line[0][0], crosspoint))
                        return True
                return False

        if first_line[1][0] == first_line[0][0] and second_line[1][0] == second_line[0][0]:
            pass
        elif first_line[1][0] == first_line[0][0]:
            deckard_equation(first_line, second_line)

        elif second_line[1][0] == second_line[0][0]:
            deckard_equation(second_line, first_line)
        else:
            a_prime = (first_line[1][1]-first_line[0][1])/(first_line[1][0]-first_line[0][0])
            b_prime = first_line[0][1] - a_prime * first_line[0][0]
            a_second = (second_line[1][1]-second_line[0][1])/(second_line[1][0]-second_line[0][0])
            b_second = second_line[0][1] - a_second * second_line[0][0]

            if not a_prime == a_second:
                crosspoint = (b_second - b_prime)/(a_prime - a_second)
                if self.line_check(first_line, crosspoint) and self.line_check(second_line, crosspoint):
                    self.collisions.append(Vec2d(crosspoint, a_prime * crosspoint + b_prime))
                    return True
            return False
