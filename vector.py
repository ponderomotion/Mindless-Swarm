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