from concurrent.futures.process import _ThreadWakeup
from math import sqrt
import pygame
import time
import mouse
import pyautogui
import keyboard

Gravity = pygame.math.Vector2(0,10)
deltaTime = 0
Points = []
Sticks = []
Positions = []
simulate = False
press = False
m_press = False
mr_press = False
MouseOn = None
pygame.init
window = pygame.display.set_mode((1920, 1080))
window.fill([0,0,0])



class Ball:
    
    def __init__(self,x,y,Locked : bool):
        self.Position = pygame.math.Vector2( x , y )
        self.prevPos = pygame.math.Vector2( x , y )

        self.Locked = Locked



class Stick:
    
    def __init__(self, point_a, point_b):
    
    
        self.Ball_a = point_a
        self.Ball_b = point_b
        
        vec = pygame.math.Vector2(point_a.Position - point_b.Position)
        
        self.Length = vec.magnitude()


def MouseCheck():
    
    global MouseOn
    MouseOnHold = None
    for x in range(0,30):
        for y in range(0,30):
            mousepos = pyautogui.position()
            cx = mousepos.x - 15 + x
            cy = mousepos.y - 15 + y
            if (cx,cy) in Positions:

                index = Positions.index((cx,cy))
                MouseOnHold = Points[index]
                
                
            
    if MouseOnHold == None:
            MouseOn = None
        
    else:
        
        MouseOn = MouseOnHold
            
            



B_A = None

B_B = None

def PointCreate():
    global B

    global B_A
    global B_B
    
    global MouseOn
    #print(Cooldown)
    mousepos = pyautogui.position()
    
    if MouseOn == None:
        
    
        if mouse.is_pressed(button='left') and m_press == False:


            B = Ball(mousepos.x,mousepos.y, False)
            Points.append(B)
            Positions.append((mousepos.x,mousepos.y))




    else:
        if mouse.is_pressed(button="left")  and m_press == False:
            if B_A == None:
                
                B_A = MouseOn
                
            else:
                
                B_B = MouseOn
                Sticks.append( Stick(B_A,B_B) )
                B_A = None
                B_B = None
        
        if mouse.is_pressed( button= "right") and mr_press == False:
            
            MouseOn.Locked = not MouseOn.Locked
                


    
    


    
        
    

def Simulate():
    global deltaTime
    for  point in Points:
        if point.Locked == False:
            
            PositionBeforeUpdate = point.Position
            
            point.Position = point.Position + (point.Position - point.prevPos)

            point.Position = point.Position +  Gravity * deltaTime
            

            
            
            point.prevPos = PositionBeforeUpdate

            
    
    for i in range(170):
    
    
        for  stick in Sticks:
            if stick.Length != 0:

                StickCentre =  (stick.Ball_a.Position + stick.Ball_b.Position) / 2
                
                StickDir = (stick.Ball_a.Position - stick.Ball_b.Position).normalize()
                
                Length = (stick.Ball_a.Position - stick.Ball_b.Position).magnitude()
                
                if Length != stick.Length:            
                
                    if stick.Ball_a.Locked != True:
                        stick.Ball_a.Position = StickCentre + StickDir * (stick.Length / 2)


                    if stick.Ball_b.Locked != True:
                        stick.Ball_b.Position = StickCentre - StickDir * (stick.Length / 2)

        
       
           

def Draw():
    for  Point in Points:
        
        #print(Point.Position)
        if Point.Locked == True:
            pygame.draw.circle(window,[255,0,0],(Point.Position.x,Point.Position.y),10,0)

        else:
            pygame.draw.circle(window,[255,255,255],(Point.Position.x,Point.Position.y),10,0)
            
    for  stick in Sticks:
        
        pygame.draw.line(window,[255,255,255],(stick.Ball_a.Position.x, stick.Ball_a.Position.y),(stick.Ball_b.Position.x, stick.Ball_b.Position.y))





while True:
    pygame.event.get()
    start_time = time.time()
    
    window.fill([0,0,0])
    MouseCheck()
    PointCreate()
    Draw()
    
    
    if mouse.is_pressed(button= "left") and m_press == False:
        m_press = True
        
    if mouse.is_pressed(button= "left") == False and m_press == True:
        m_press = False
    
    if mouse.is_pressed(button= "left") and m_press == True:
        m_press = True
        
    if mouse.is_pressed(button= "right") and mr_press == False:
        mr_press = True
        
    if mouse.is_pressed(button= "right") == False and mr_press == True:
        mr_press = False
    
    if mouse.is_pressed(button= "right") and mr_press == True:
        mr_press == True

    if keyboard.is_pressed("s") and press == False:
        simulate = not simulate
        press = True
        
    if keyboard.is_pressed("s") == False:
        press = False
    
    if simulate == True:
        Simulate()
    
    
    pygame.display.flip()
    
    end_time = time.time()
    deltaTime = end_time - start_time
    Fps = (1 / (deltaTime + 0.00000000000000001)) 
    #print(Fps)
    print(m_press)
    if keyboard.is_pressed("escape"):
        break

pygame.display.quit




