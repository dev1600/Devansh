from  matplotlib import pyplot as plt
import numpy as  np
import  math
import random
from matplotlib.animation import  FuncAnimation
import time
from itertools import count
from plot_import import*
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
# plt.style.use('seaborn')
# x=np.linspace(0,100,10000)

# if 
#     y=np.sin(3*3.141*x)
x=[]
y=[]
index=count()
class Communicate(QObject):
    s=pyqtSignal(int)
    
class Current():
    
    def __init__(self):
        
        o=obj()
        comm.s.connect(o.display)
        
        
    def getRandomAribitary(self,min,max):
        return random.random()*(max-min)+min

    def animate(self,i):
        # z=int(index)
        # static z=0
        # t1=time.time(
        # z=list(next(count) for _ in range(10))
        if (i==0):
            x.append(next(index))
            y.append(0)
        
        elif (i==1):
            x.append(next(index))
            y.append(0.15)
            
            
        elif (i%20==0 or i%20==1 ):
            if(i<25):
                comm.s.emit(12)
                x.append(next(index))
                y.append(self.getRandomAribitary(2,2.25))
            
            # print(index)
                
            
        elif (i>25):
            x.append(next(index))
            y.append(self.getRandomAribitary(-0.06,0.06))
        elif (i<25):
            x.append(next(index))
            y.append(self.getRandomAribitary(0.3,0.4))
            time.sleep(0.1)
            
        # print(i)
        # print(index)
        
        plt.cla()
        # plt.xlim(0,5)
        plt.ylim(-3,3)
        plt.plot(x,y)
        plt.axhline(y=0,color='k')
        plt.tight_layout()
        # z=z+1
        # print(z)

if __name__=="__main__": 
    comm=Communicate()  
    xyz=Current()
    ani=FuncAnimation(plt.gcf(),xyz.animate,interval=100)

# while (x<10000):
#     if(x%100==0):
#         y.append(getRandomAribitary(2,2.5))
#     else: y.append(getRandomAribitary(0.95,1.05))
#     # y.append(getRandomAribitary(0.95,1.05))
#     z.append(x)
#     x=x+1

# print(y)

    

# plt.plot(x,y)
plt.show()

