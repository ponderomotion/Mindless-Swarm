# Laika
# Daniel Fletcher 2013
# License: 
#    Creative Commons Attribution - Non-Commercial - NoDerivs 2.0 England and Wales
#    See LICENSE for details

from math import sin, cos, radians


class Vec2d():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def to_tuple(self):
		return self.x, self.y
	def rotate(self, degrees, origin):
		theta = radians(degrees)
		newx = origin.x + ((self.x - origin.x) * cos(theta) - (self.y - origin.y) * sin(theta))
		newy = origin.y + ((self.x - origin.x) * sin(theta) + (self.y - origin.y) * cos(theta))
		return newx,newy
	def __add__(self,other):
		return Vec2d(self.x + other.x, self.y + other.y)