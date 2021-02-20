import socket
import pygame
import os
import time
import threading
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5 import uic
import sys
import cv2


HEADER =100
# PORT =5050
# Below is port for LAN to UART
PORT=5005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE ="!DISCONNECT"
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
axis = {}
button = {}


class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def TakeScreenshot(self):
        ps4.logic = 1

    def setFullScreen(self):
        if ps4.full_screen == 1:
            ps4.full_screen = 0
        else:
            ps4.full_screen = 1

    def run(self):
        cap = cv2.VideoCapture(0)
        value = 0
        while True:
            ret, frame = cap.read()
            if ret:

                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                
                if ps4.full_screen == 0:
                    p = convertToQtFormat.scaled(720,1280, Qt.KeepAspectRatio)
                else:
                    p = convertToQtFormat.scaled(620, 480, Qt.KeepAspectRatio)

                self.changePixmap.emit(p)
                if ps4.logic == 1:
                    value += 1
                    cv2.imwrite(
                        'C:/Users/Devansh/Python/PyQt5 Codes/PyQt5 Designer/Screenshot/CamPhotoNo.%s.png' % (value), frame)
                    Camera.logic = 0
                    print("SS taken")
    
class ps4(QMainWindow):
    speak=pyqtSignal(str)
    
    logic = 0
    full_screen = 0
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.joystick.init()
        comm = Comm()
        self.speak.connect(self.setTerminal)

        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        global a
        a=uic.loadUi(r"C:\Users\devan\OneDrive\Documents\Python\GUI\UI\MRM_2021.ui", self)
        
    def setup(self):
        # Three types of controls: axis, button, and hat
        
        for i in range(self.controller.get_numaxes()):
            axis[i] = 0.0
            # Buttons are initialized to False
        for i in range(self.controller.get_numbuttons()):
            button[i] = False
            
        self.control()

    # Main loop, one can press the PS button to break
    def control(self):
        self.quit = False
        while self.quit == False:

            # Get events
            for event in pygame.event.get():

                if event.type == pygame.JOYAXISMOTION:
                    axis[event.axis] = round(event.value,3)
                elif event.type == pygame.JOYBUTTONDOWN:
                    button[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    button[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    hat[event.hat] = event.value

            self.quit = button[BUTTON_PS]
            self.display()

        
    def display(self):
            os.system('cls')
            # comm.send(str(axis[AXIS_LEFT_STICK_X]*8000))
            # comm.send('ppppppppm')
            # time.sleep(1)
            
            # -1 cause DS4 values  are inverted
            x=str(int(-1*axis[AXIS_RIGHT_STICK_X]*8000+8000))
            y=str(int(-1*axis[AXIS_RIGHT_STICK_Y]*(8000)+8000))
            # print(x)
            x=x.zfill(5)
            y=y.zfill(5)
            # print(x)
            self.x_axis.setText(x)
            self.y_axis.setText(y)
            
            msg="m6s"+x+"f"+y+"n"
            comm.send(msg)
            print(msg)
            # comm.send("m")

            global c
            c=self.camera_box.currentIndex()
            
            if(button[BUTTON_CIRCLE]==True):
                
                self.speak.emit("Current FUcked")   
                
            elif(button[BUTTON_CIRCLE]==False):
                self.speak.emit("Current Bueno") 
                
            # print("Left stick X:", axis[AXIS_LEFT_STICK_X])
            # print("Left stick Y:", axis[AXIS_LEFT_STICK_Y])
            # print("Right stick X:", axis[AXIS_RIGHT_STICK_X])
            # print("Right stick Y:", axis[AXIS_RIGHT_STICK_Y])
            # print("L2 strength:", axis[AXIS_L2])
            # print("R2 strength:", axis[AXIS_R2],"\n")
            # # Buttons
            # print("Square:", button[BUTTON_SQUARE])
            # print("Cross:", button[BUTTON_CROSS])
            # print("Circle:", button[BUTTON_CIRCLE])
            # print("Triangle:", button[BUTTON_TRIANGLE])
            # print("L1:", button[BUTTON_L1])
            # print("R1:", button[BUTTON_R1])
            # print("L2:", button[BUTTON_L2])
            # print("R2:", button[BUTTON_R2])
            # print("Share:", button[BUTTON_SHARE])
            # print("Options:", button[BUTTON_OPTIONS])
            # print("PS:", button[BUTTON_PS])
            # print("Touch Pad:", button[BUTTON_PAD],"\n")


            # print("Press PS button to quit:", quit)

            # Limited to 30 frames per second to make the display not so flashy
            clock = pygame.time.Clock()
            clock.tick(30) 
    
    
    def image(self):                
        th=CameraThread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        a.screenshot.pressed.connect(CameraThread.TakeScreenshot)
        
    pyqtSlot(QImage)
    def setImage(self,image):
        if(c == 1):
            a.main_camera.setPixmap(QPixmap.fromImage(image))
        
        a.camera_2.setPixmap(QPixmap.fromImage(image))
    
    pyqtSlot(str)
    def setTerminal(self,s):
        a.terminal.setPlainText(s)
        
class Comm():
    
    def __init__(self):
        
        # self.SERVER = socket.gethostbyname(socket.gethostname())
        # Below is IP for LAN to UART
        self.SERVER="192.168.1.7"
        self.ADDR=(self.SERVER,PORT)
        self.client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        # ps4.a.camera_2.setText("Hello")

    def send(self,msg):
        self.message=msg.encode(FORMAT)
        # self.msg_length=len(self.message)
        # self.send_length=str(self.msg_length).encode(FORMAT)
        
        #We are padding spaces to make message 64 bytes
        # self.send_length +=b' '*(HEADER-len(self.send_length))
        # self.client.send(self.send_length)
        self.client.sendall(self.message)


app = QApplication(sys.argv)
mainWindow = ps4()


mainWindow.image()


widget = QStackedWidget()
widget.addWidget(mainWindow)
widget.show()


comm=Comm()
# comm.send("Hello World")
# comm.send("Hello Apoogggrv")
# comm.send("Hello Bitchhjytr!")  

t1=threading.Thread(target=mainWindow.setup, args=())
t1.start()
# comm.send("lfdgon")
app.exec_()
comm.send(DISCONNECT_MESSAGE)