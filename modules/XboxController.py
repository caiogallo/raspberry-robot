from evdev import InputDevice, categorize, ecodes
import sys
import logging

sys.path.append("../")
import Constants

xboxButtonMap = {
        'ABS_GAS': Constants.EventType.FORWARD,
        'ABS_X': Constants.EventType.DIRECTION,
        'ABS_HAT0X': Constants.EventType.DPAD_DIRECTION
    }



class XboxController():
    logging.basicConfig(level=logging.DEBUG)
    
    def __init__(self, event_callback):
        self.event_callback = event_callback
        
        self.gamepad = InputDevice('/dev/input/event0')
        
        logging.info('Xbox Device: ' + str(self.gamepad.name))
        
        for event in self.gamepad.read_loop():
            if event.type == ecodes.EV_KEY:
                print(event)
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                xboxButton = ecodes.bytype[absevent.event.type][absevent.event.code]
                
                try:
                    button = xboxButtonMap[xboxButton]
                    
                    value = 0
                    if(button == Constants.EventType.FORWARD):
                        value = absevent.event.value / 1024
                    elif(button == Constants.EventType.DPAD_DIRECTION):
                        if(absevent.event.value > 0):
                            value = 1
                        elif(absevent.event.value < 0):
                            value = -1
                        else:
                            value = 0
                                        
                    self.event_callback(button, value)
                except Exception as e:
                    logging.debug('button ' + xboxButton + ' not mapped, exception: ' + str(e))




