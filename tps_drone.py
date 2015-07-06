import contextlib
import functools
import itertools
import logging
import sys
import time
import turtle

logging.basicConfig(level=logging.ERROR, stream=sys.stdout)

GROUNDED = 'grounded'
IN_FLIGHT = 'in_flight'
TURT = None
MOVE_AMOUNT = 10

def turtle_factory(*args, **kwargs):
    """For our purposes we will limit ourselves to one drone.
    To be able to clear the old path, we need to keep the
    previous drone around. So we use a singleton"""
    global TURT
    if not TURT:
        TURT = turtle.Turtle()
    return TURT


class TPSDrone:
    def __init__(self):
        self.t = turtle_factory()
        self.t.hideturtle()
        self.t.showturtle()
        self._name = 'Turtle Drone {}'.format(id(self))
        self.navdata = {'battery': 100}
        self._speed = 0.2 # 0-1 how long to go MOVE_AMOUNT px
        self._state = GROUNDED
        self._commands = []
        logging.info('Coonection to trdrone')
        logging.info('Coonection established')

    def startup(self):
        pass

    def shutdown(self):
        pass

    def reset(self):
        self.land()
        self.t.reset()

    def takeoff(self):
        """Make the drone takeoff."""
        self.t.pendown()
        self.t.shapesize(2, 2)
        self.t.dot()
        self._state = IN_FLIGHT
        self._commands.append('takeoff')

    def land(self):
        self.t.pensize(1)
        self.t.shapesize(1, 1)
        self.t.dot()
        self.t.penup()
        self._state = GROUNDED
        self._commands.append('land')

    def hover(self):
        """Make the drone hover."""
        pass

    def moveLeft(self):
        """Make the drone move left."""
        self.t.left(90)
        self.t.forward(MOVE_AMOUNT)
        self.t.right(90)

    def moveRight(self):
        """Make the drone move right."""
        self.t.right(90)
        self.t.forward(MOVE_AMOUNT)
        self.t.left(90)

    def moveUp(self):
        """Make the drone rise upwards."""
        w, h, _ = self.t.shapesize()
        self.t.shapesize(w+1, y+1)
        self.draw_battery()

    def moveDown(self):
        """Make the drone decent downwards."""
        w, h, _ = self.t.shapesize()
        self.t.shapesize(w-1, y-1)
        self.draw_battery()

    def moveForward(self):
        """Make the drone move forward."""
        if self._state == GROUNDED:
            logging.info('Please takeoff')
        else:
            self.t.forward(MOVE_AMOUNT)
            self.draw_battery()

    def moveBackward(self):
        """Make the drone move backwards."""
        if self._state == GROUNDED:
            logging.info('Please takeoff')
        else:
            self.t.backward(MOVE_AMOUNT)
            self.draw_battery()

    def turnLeft(self):
        """Make the drone rotate left."""
        self.t.left(5)
        self.draw_battery()

    def turnRight(self):
        """Make the drone rotate right."""
        self.t.right(5)
        self.draw_battery()



    def setSpeed(self, speed):
        """Set the drone's speed.

        Valid values are floats from [0..1]

        Maps them to turtle speed 1-10
        """
        self.t.speed(max(10, int(speed*10)))

    # bonus features
    def write(self, txt):
        self.t.write(txt)

    def draw_battery(self):
        power = self.navdata['battery']
        self.navdata['battery'] -= 1

    @property
    def name(self):
        return self._name

    @property
    def commands(self):
        return self._commands

def hello_world():
    d = TPSDrone()
    d.takeoff()
    return d
