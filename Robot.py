import logging
from threading import Thread
from time import sleep

from modules.Engine import Engine
from modules.Rcon import Rcon
from modules.XboxController import XboxController
import Constants

leftPins = (2,3,4)
rightPins = (17,22,27)

class Robot():
       
    def setupEngines(self):
        logging.info('setup engines')
        logging.debug('left engine pins ' + str(leftPins))
        logging.debug('right engine pins ' + str(rightPins))
        
        self.leftEngines = Engine(leftPins[0], leftPins[1], leftPins[2])
        self.rightEngines = Engine(rightPins[0], rightPins[1], rightPins[2])
        self.direction = 0
        
    def selfTest(self):
        logging.debug('initializing self-test')
        logging.debug('move left engines forward')
        self.leftEngines.move()
        self.leftEngines.stop()
        
        logging.debug('move right engines forward')
        self.rightEngines.move()
        self.rightEngines.stop()
        
    def rconReceiveDataCallback(self, data):
        logging.debug('received data: ' + str(data))
        
        if str(data) == 'forward':
            self.moveForward()
            
            
    def inputEventCallback(self, eventType: Constants.EventType, value):
        logging.debug(eventType.name + ', ' + str(value))
        
        if(eventType == Constants.EventType.DPAD_DIRECTION):
            self.direction = value
        
        if(eventType == Constants.EventType.FORWARD):
            if(value >= 0.001):
                self.moveForward(speed = value, direction = self.direction)
            else:
                self.stopEngines()
        
        
    def moveForward(self, speed = 10, direction = 0):
        leftSpeed = speed
        rightSpeed = speed
        if(direction < 0):
            leftSpeed = speed * 0.5
        elif(direction > 0):
            rightSpeed = speed * 0.5
            
        logging.debug('moving forward with speed [left=' + str(leftSpeed) + ',right=' + str(rightSpeed) + ', direction = ' + str(direction))
        self.rightEngines.move(speed = speed)
        self.leftEngines.move(speed = speed)
        
    def stopEngines(self):
        logging.debug('engines stopped')
        self.rightEngines.stop()
        self.leftEngines.stop()
        
    def startRconServer(self):
        Rcon(self.rconReceiveDataCallback)
        
    def startXboxController(self):
        XboxController(self.inputEventCallback)
        
def main():
    logging.basicConfig(level=logging.DEBUG)
    robot = Robot()
    robot.setupEngines()
    Thread(target=robot.startRconServer).start()
    Thread(target=robot.startXboxController).start()
    
if __name__ == '__main__':
    main()
    
