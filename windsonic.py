import serial
import sys
import time
from os import path

descriptor =  input("Please enter descriptor for this test (no special characters)")

dataIter = 1
dataName_base = "test_"
descriptorNS = descriptor.replace(' ', '_')
dataName = dataName_base + descriptorNS + "_1"

#FILE CREATION AND HEADERS
log = True
if log:
    while path.exists(dataName + ".txt"): #Check to see if our new file name is unique
        dataName = dataName_base + str(dataIter + 1) #If not unique incriment file name
        dataIter = dataIter + 1 #...Iter
    f = open(dataName+".txt", "w") #Create unique file
    f.write("test " + str(dataIter) + " Windsonic sensor\n")
    f.write("Descriptor, :" + descriptor)
    f.write("DATA FORMAT\n")
    f.write("Format, Wind Direction, Wind Speed, Units, Status, Checksum\n")

#DATA LOGGING SECTION
ser = serial.Serial('/dev/ttyUSB0', 38400)

input("Serial connectio established, press enter to begin logging")

while True: #Logging loop
    try:

        #Only log when switch is active
        newDat = ser.readline()
        newDat2 = newDat.replace(b"<STX>", b"")
        newDat3 = newDat.replace(b"<ETX>", b"")
        # byteChk = utf8len(newDat3)
        toWrite = str(time.process_time()) + "," + str(newDat3)
        f.write(toWrite + "\n")
        sys.stdout.write(toWrite+"\r")
        sys.stdout.flush()
            

    except KeyboardInterrupt:
        print("Pressed Ctrl-C to terminate while statement")
        break


#ENDGAME 
f.close()                  #⛔⛔⛔⛔ CLOSE FILE
