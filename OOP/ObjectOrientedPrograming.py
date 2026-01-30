import math
class Point:
    'Represents a point in two-dimesional geometric coordinates'

    def __init__(self, x=0, y=0):
        '''Initialize the position of new point. The x and y coordinates
        can be specified. If they are not, the point defaults to the origin.'''
        self.move(x,y)
    def move(self, x, y):
        "Move the point to a new location in 2D space."
        self.x=x
        self.y=y
    def reset(self):
        'Reset the point poac to the geometric origin: 0, 0'
        self.move(0, 0)
    def calculate_distance(self, other_point):
        """Calculate the distance from this point to a second point passed as parameter
        This function uses the Pythagorean Theorem to calculate the distance between the two points.
        The distance is returned as float"""
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2

