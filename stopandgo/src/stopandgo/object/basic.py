import math
from pygame import mouse
from stopandgo import graphics, object

class Sprite(object.GameObject):
    '''
    A simple world object combining a single image with some basic motion machinery.
    '''

    def __init__(self, sprite, loc = (0, 0), maxspeed = 2, overshoot = 0.05):
        object.GameObject.__init__(self, sprite, loc)
        self.maxspeed = maxspeed
        self.overshoot = overshoot
    
    def move(self, x, y):
        '''
        Move the sprite the specified displacement, at full speed.
        '''
        startloc = self.loc
        steps = int(math.ceil(math.sqrt(x*x + y*y)/self.maxspeed - self.overshoot))
        for i in xrange(steps - 1):
            self.loc = (startloc[0] + i*x/steps, startloc[1] + i*y/steps)
            self.display()
        self.loc = (startloc[0] + x, startloc[1] + y)
        self.display()
    
    def leap(self, absx, absy):
        '''
        Teleport the sprite to the specified location, regardless of distance.
        '''
        self.loc = (absx, absy)
        self.display()


class BallPatrollingDiamond(Sprite):
    def __init__(self, loc, maxspeed=math.sqrt(8), diamondradius=60):
        Sprite.__init__(self, graphics.ball, loc=loc, maxspeed=maxspeed)
        self.diamondradius = diamondradius
        
    def ai(self):
        dr = self.diamondradius
        while True:
            self.move(dr, -dr)
            self.move(dr, dr)
            self.move(-dr, dr)
            self.move(-dr, -dr)

class BallPatrollingCircle(Sprite):
    def __init__(self, loc, startangle=0, radius=60, speed=60*math.pi/100):
        Sprite.__init__(self, graphics.ball, loc=loc)
        self.startangle = startangle
        self.radius = radius
        self.arcspeed = speed / radius
        self.center = (self.loc[0] - self.radius*math.cos(self.startangle),
                       self.loc[1] - self.radius*math.sin(self.startangle))
    
    def ai(self):
        theta = self.startangle
        while True:
            self.leap(self.center[0] + self.radius*math.cos(theta),
                      self.center[1] + self.radius*math.sin(theta))
            theta += self.arcspeed

class BallFollowingMouse(Sprite):
    def __init__(self):
        Sprite.__init__(self, graphics.ball)
        
    def ai(self):
        while True:
            self.leap(*mouse.get_pos())
