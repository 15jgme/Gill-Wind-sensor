import serial
import sys
import os.path
from os import path

from gpiozero import Button

ser = serial.Serial('COM4')


dataIter = 1
dataName_base = "test_"
dataName = "test_1"

def utf8len(s): #For counting bytes for checksum
    return len(s.encode('utf-8'))

#Want to only log data when switch on gpio

switch = Button(4) #Init switch for data logging

log = True
if log:
    while path.exists(dataName + ".txt"): #Check to see if our new file name is unique
        dataName = dataName_base + str(dataIter + 1) #If not unique incriment file name
    f = open(dataName+".txt", "w") #Create unique file
    f.write("test " + str(dataIter) + "Windsonic sensor")
    f.write("DATA FORMAT")
    f.write("Format, Wind Direction, Wind Speed, Units, Status, Checksum")


try:
    while True:
        newDat = ser.readline()
        newDat2 = newDat.replace("<STX>", "")
        newDat3 = newDat.replace("<ETX>", "")
        byteChk = utf8len(newDat3)
        f.write(newDat3)
        sys.stdout.write(newDat3+"\r")
        sys.stdout.flush()

except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass



