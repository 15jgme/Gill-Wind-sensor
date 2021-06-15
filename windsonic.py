import serial
import sys
import os.path
import time
from os import path

from gpiozero import Button

ser = serial.Serial('/dev/ttyUSB0', 38400)


dataIter = 1
dataName_base = "test_"
dataName = "test_1"


#FILE CREATION AND HEADERS
log = True
if log:
    while path.exists(dataName + ".txt"): #Check to see if our new file name is unique
        dataName = dataName_base + str(dataIter + 1) #If not unique incriment file name
        dataIter = dataIter + 1 #...Iter
    f = open(dataName+".txt", "w") #Create unique file
    f.write("test " + str(dataIter) + " Windsonic sensor\n")
    f.write("DATA FORMAT\n")
    f.write("Format, Wind Direction, Wind Speed, Units, Status, Checksum\n")

#DATA LOGGING SECTION
while True: #Logging loop
    try:
        #print(switch.is_pressed)
        if switch1.is_pressed: #Logging switch is flicked 
            #Only log when switch is active
            newDat = ser.readline()
            newDat2 = newDat.replace(b"<STX>", b"")
            newDat3 = newDat.replace(b"<ETX>", b"")
            # byteChk = utf8len(newDat3)
            toWrite = str(time.process_time()) + "," + str(newDat3)
            f.write(toWrite + "\n")
            sys.stdout.write(toWrite+"\r")
            sys.stdout.flush()
            
            if ledInd % 40 == 0:
                ledOn()

            if ledInd % 19 == 0:
                ledOff()
        
        elif switch1.is_pressed: #Kill switch is flicked 
            break #Head to the end of the program where the file is closed and system is shutdown
            
    
    except KeyboardInterrupt:
        print("Pressed Ctrl-C to terminate while statement")
        break


#ENDGAME 
f.clsoe()                  #⛔⛔⛔⛔ CLOSE FILE
os.system("sudo shutdown") #☠️☠️☠️☠️ KILL