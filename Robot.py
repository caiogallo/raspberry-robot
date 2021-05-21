import logging
from time import sleep

from Engine import Engine

leftPins = (2,3,4)
rightPins = (17,22,27)

class Robot():

    def setupEngines(self):
        logging.info('setup engines')
        logging.debug('left engine pins ' + str(leftPins))
        logging.debug('right engine pins ' + str(rightPins))
        
        self.leftEngines = Engine(leftPins[0], leftPins[1], leftPins[2])
        self.rightEngines = Engine(rightPins[0], rightPins[1], rightPins[2])
        
    def selfTest(self):
        if(logging.level == logging.DEBUG):
            logging.debug('initializing self-test')
            logging.debug('move left engines forward for 2 seconds')
            self.leftEngines.move()
            sleep(2)
            self.leftEngines.stop()
            
            logging.debug('move right engines forward for 2 seconds')
            self.rightEngines.move()
            sleep(2)
            self.rightEngines.stop()


def main():
    logging.basicConfig(level=logging.DEBUG)
    robot = Robot()
    robot.setupEngines()
    robot.selfTest()
    
if __name__ == '__main__':
    main()
    