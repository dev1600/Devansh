# Use pygame to get readouts from a ds4 controller
# This is an efficient way to get inputs as long as you don't need six-axis data

import pygame
import os
import time
import threading

AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 2
AXIS_RIGHT_STICK_Y = 3
AXIS_R2 = 4
AXIS_L2 = 5
# Labels for DS4 controller buttons
# # Note that there are 14 buttons (0 to 13 for pygame, 1 to 14 for Windows setup)
BUTTON_SQUARE = 2
BUTTON_CROSS = 0
BUTTON_CIRCLE = 1
BUTTON_TRIANGLE = 3
BUTTON_L1 = 9
BUTTON_R1 = 10
BUTTON_L2 = 7
BUTTON_R2 = 8
BUTTON_SHARE = 8
BUTTON_OPTIONS = 6

BUTTON_LEFT_STICK = 10
BUTTON_RIGHT_STICK = 11

UP_ARROW=11
DOWN_ARROW=12
LEFT_ARROW=13
RIGHT_ARROW=14

BUTTON_PS = 5
BUTTON_PAD = 15



class ps4():
    
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.setup()

    def setup(self):
        # Three types of controls: axis, button, and hat
            self.axis = {}
            self.button = {}
            self.hat = {}

            # Assign initial data values
            # Axes are initialized to 0.0
            for i in range(self.controller.get_numaxes()):
                self.axis[i] = 0.0
            # Buttons are initialized to False
            for i in range(self.controller.get_numbuttons()):
                self.button[i] = False
            # Hats are initialized to 0
        

            # Labels for DS4 controller axes
            
            # Labels for DS4 controller hats (Only one hat control)
            # HAT_1 = 0
            self.control()

    # Main loop, one can press the PS button to break
    def control(self):
        self.quit = False
        while self.quit == False:

            # Get events
            for event in pygame.event.get():

                if event.type == pygame.JOYAXISMOTION:
                    self.axis[event.axis] = round(event.value,3)
                    # print("Trueeeee")
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat[event.hat] = event.value
                    print(event.value)
                    # if event.hat ==0:
                    #     if event.value ==(1,0):
                    #         print("Right")

            self.quit = self.button[BUTTON_PS]
            self.display()

        # Print out results
        
        # Axes
    def display(self):
            os.system('cls')
            print("Left stick X:", self.axis[AXIS_LEFT_STICK_X])
            print("Left stick Y:", self.axis[AXIS_LEFT_STICK_Y])
            print("Right stick X:", self.axis[AXIS_RIGHT_STICK_X])
            print("Right stick Y:", self.axis[AXIS_RIGHT_STICK_Y])
            print("L2 strength:", self.axis[AXIS_L2])
            print("R2 strength:", self.axis[AXIS_R2],"\n")
            # Buttons
            print("Square:", self.button[BUTTON_SQUARE])
            print("Cross:", self.button[BUTTON_CROSS])
            print("Circle:", self.button[BUTTON_CIRCLE])
            print("Triangle:", self.button[BUTTON_TRIANGLE])
            print("L1:", self.button[BUTTON_L1])
            print("R1:", self.button[BUTTON_R1])
            print("L2:", self.button[BUTTON_L2])
            print("R2:", self.button[BUTTON_R2])
            print("Share:", self.button[BUTTON_SHARE])
            print("Options:", self.button[BUTTON_OPTIONS])
            # print("Left stick press:", button[BUTTON_LEFT_STICK])
            # print("Right stick press:", button[BUTTON_RIGHT_STICK])
            print("PS:", self.button[BUTTON_PS])
            print("Touch Pad:", self.button[BUTTON_PAD],"\n")
            print("UP ARROW:",self.button[UP_ARROW])
            print("DOWN ARROW:",self.button[DOWN_ARROW])
            print("LEFT ARROW:",self.button[LEFT_ARROW])
            print("RIGHT ARROW:",self.button[RIGHT_ARROW])
            # print("Hat X:", self.hat[HAT_1][0])
            # print("Hat Y:", self.hat[HAT_1][1],"\n")
            # # Hats
            # print("JOY",pygame.event.get())
            # print("Hat X:", self.hat)
            # print("HAT :",event.type)6
            # print("Hat Y:", self.hat[1],"\n")
            # print("Hat :",self.controller.get_hat(0))

            print("Press PS button to quit:", quit)

            # Limited to 30 frames per second to make the display not so flashy
            clock = pygame.time.Clock()
            clock.tick(30) 
            # time.sleep(0.5)
cont=ps4()

        
