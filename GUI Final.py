'''
So this is a simple project to map a serial input (from say an arduino) and map it onto a circular dial.
It also displays the raw digital data in a box within the dial much like a car system.
'''
import math
#import serial
import time
#Just making sure it works on both Python 2 and 3 without a hitch!
try:
    from Tkinter import *
    from Tkinter.font import Font
    import Tkinter.filedialog
    import Tkinter.messagebox
except ImportError:
    from tkinter import *
    from tkinter.font import Font
    import tkinter.filedialog
    import tkinter.messagebox



# parameters
#ser=serial.Serial('COM7',9600) #Check which port your device is connected to and change it accordingly.
width,height = 400,400 #Dimensions of the canvas.
len1,len2 = 0.85,0.3 #Dimensions of the needle, relative to the canvas ray.
ray = int(0.7*width/2) #Radius of the dial.
rayR=int(0.5*width/2)
x0,y0 = width/2,width/2 #Position of the center of the circle.
min_speed,max_speed = 0,260 #Max and min values on the dial. Adjust according to need.
step_speed = 20 #Least count or smallest division on the dial which has a text value displayed. Adjust according to need.
min_rpm,max_rpm = 0,10 #Max and min values on the dial. Adjust according to need.
step_rpm = 1#Least count or smallest division on the dial which has a text value displayed. Adjust according to need.

root = Tk()

meter_font = Font(family="DS-Digital",size=18,weight='normal')#The font used in the meter. Feel free to play around.
#temp=ser.readline()#Take the first reading as a temp/garbage value so that it doesn't mess up the program.

#Set the titles of the window, dials etc.
def setTitles(): 
    root.title('Zuura')
    #speed.itemconfig(speed.title,text='Speed')
    speed.itemconfig(speed.unit,text='KMPH')
    #rpm.itemconfig(rpm.title,text='RPM')
    rpm.itemconfig(rpm.unit,text='x1000')

class Meter(Canvas):

    def draw(self,vmin,vmax,step,title,unit, isRpm):
        self.vmin = vmin
        self.vmax = vmax

        x0 = width/2
        y0 = width/2

        
        ray = int(0.8*width/2)
        if(isRpm):
            ray=int(0.5*width/2)
            x0=x0-90
            y0=y0+70
            coord = x0-ray, y0-ray, x0+ray+30, y0+ray+30
            arc = self.create_arc(coord, start=-20, extent=80, fill="red")
        self.title = self.create_text(width/2,12,fill="white",
            font=meter_font) #Meter title.
        self.create_oval(x0-ray*1.1,y0-ray*1.1,x0+ray*1.1,y0+ray*1.1,
            fill="blue")#The blue outer ring.
        self.create_oval(x0-ray*1.1,y0-ray*1.1,x0+ray*1.1,y0+ray*1.1,
            fill="blue")#The blue outer ring.
        self.create_oval(x0-ray,y0-ray,x0+ray,y0+ray,fill="#000")#The dial.
        coef = .5
        self.create_oval(x0-ray*coef,y0-ray*coef,x0+ray*coef,y0+ray*coef,
            fill="blue")#This is the connection point blob of the needle.

        #This loop fills in the values at each step or gradation of the dial.
        for i in range(2,1+int((vmax-vmin)/step)):
            v = vmin + int(step*(i-2))
            angle = (5+6*((v-vmin)/(vmax-vmin)))*math.pi/3.75
            self.create_line(x0+ray*math.sin(angle)*0.9,
                y0 - ray*math.cos(angle)*0.9,
                x0+ray*math.sin(angle)*0.98,
                y0 - ray*math.cos(angle)*0.98,fill="#FFF",width=2)#Major div
            self.create_text(x0+ray*math.sin(angle)*0.75,
                y0 - ray*math.cos(angle)*0.75,
                text=v,fill="#FFF",font=meter_font)#Numbers inside meter
            if i==int(vmax-vmin)/step:
                continue
            for dv in range(1,5):
                angle = (5+6*(v+dv*(step/5)-vmin)/(vmax-vmin))*math.pi/3.75
                self.create_line(x0+ray*math.sin(angle)*0.94,
                    y0 - ray*math.cos(angle)*0.94,
                    x0+ray*math.sin(angle)*0.98,
                    y0 - ray*math.cos(angle)*0.98,fill="#FFF")#Minor Div
        self.unit = self.create_text(x0,y0+0.8*ray,fill="#FFF",
            font=meter_font)#Text inside meter
        self.needle = self.create_line(x0-ray*math.sin(5*math.pi/4)*len2,
            y0+ray*math.cos(5*math.pi/4)*len2,
            x0+ray*math.sin(5*math.pi/4)*len1,
            y0-ray*math.cos(5*math.pi/4)*len1,
            width=5,fill="blue")#Needle
      #  lb1=Label(self, compound='right', textvariable=v)

    #Draws the needle based on the speed or input value.
    def draw_needle(self,v, isRpm):
        #coord = 10, 50, 240, 210
        #arc = self.create_arc(coord, start=0, extent=150, fill="blue")
        
        print(v) #Not required, but helps in debugging.
        v = max(v,self.vmin)#If input is less than 0 then the pointer stays at 0
        v = min(v,self.vmax)#If input is greater than the greatest value then the pointer stays at the maximum value.
        angle = (5+6*((v-self.vmin)/(self.vmax-self.vmin)))*math.pi/3.75
        if(isRpm):
            k=0.4
            x00=x0-90
            y00=y0+70
            
            self.coords(self.needle,x00-int(k*width/2)*math.sin(angle)*len2,
                y00+int(k*width/2)*math.cos(angle)*len2,
                x00+int(k*width/2)*math.sin(angle)*len1,
                y00-int(k*width/2)*math.cos(angle)*len1)
        else:
            self.coords(self.needle,x0-ray*math.sin(angle)*len2,
                y0+ray*math.cos(angle)*len2,
                x0+ray*math.sin(angle)*len1,
                y0-ray*math.cos(angle)*len1)
        #self.tag_lower(oval)


#Setting up the meters.

meters = Frame(root,width=2*width,height=height,bg="red")
speed = Meter(meters,width=width,height=height,bg="black",highlightthickness=0)
speed.draw(min_speed,max_speed,step_speed,"Speed","KMPH",False)
speed.pack(side=LEFT)
rpm = Meter(meters,width=width,height=height,bg="black",highlightthickness=0)
rpm.draw(min_rpm,max_rpm,step_rpm,"RPM","x1000",True)
rpm.pack(side=RIGHT)
meters.pack(anchor=SE,fill=Y,expand=True)
setTitles()

# Digital value zone.
values_font = Font(family="DS-Digital",size=25,weight='normal')
cSpeed=Canvas(root, width=30, height=30,bg="white")
cSpeed.place(x=width/2.5,y=height/2.3)

x=Message(cSpeed, width = 100,text='',font=values_font,bg='blue',fg='white')
x.place(x=0,y=0)
x.pack()
cRpm=Canvas(root, width=30, height=30,bg="white")
cRpm.place(x=width+width/5.7,y=height*0.62)

gearPosSize=70
gearPos=Canvas(root,width=gearPosSize,height=gearPosSize,bg='red')
gearPos.place(x=400,y=50)
gr=Message(gearPos, width=gearPosSize, text='', font=values_font,bg='red',fg='white')
gr.pack()

y=Message(cRpm, width = 100,text='',font=meter_font, bg='blue',fg='white')
y.place(x=0,y=0)
y.pack()
rev=0
kmph=219
#The update loop. I agree this can be done better but I like this method.
while True:
    s=ser.readline()
    arr=s.split();
    time.sleep(0.1)
    v=StringVar()
    kmph=(int)(arr[0])
    rev=(int)(arr[1])
    rev=rev+100
    kmph=kmph+1
    if(rev>8000):
        rev=0
    if(kmph>220):
        kmph=0
    speed.draw_needle(kmph,False)
    rpm.draw_needle(rev/1000,True)
    x.config(text=kmph,justify='center')
    y.config(text=rev)
    gr.config(text='3')
    root.update_idletasks()
    root.update()

    
