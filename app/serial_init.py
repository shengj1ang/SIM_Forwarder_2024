# -*- coding: utf-8 -*
 
import serial
import serial.tools.list_ports
 
port_list = list(serial.tools.list_ports.comports())
List_CH340=[]
for i in port_list:
    #print(i)
    if "CH340" in str(i):
        List_CH340.append(i)

for j in List_CH340:
    print(j)