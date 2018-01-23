import serial
from datetime import datetime
s=serial.Serial('/dev/ttyACM0',9600)
s.readline()
with open('cardata.txt','w') as f:
	while 1:
    		a=s.readline()
    		b=str(datetime.now())
    		c=a+b+"\t"    
    		f.write(c)
 
