import serial
import sys
import time
from os import path
from datetime import datetime

from threading import Thread



datTime = datetime.now() # current date and time
dat = "hr_" + datTime.strftime("%H") + "_min_" + datTime.strftime("%M") + "_sec_" + datTime.strftime("%S")  + "d_" + datTime.strftime("%d") + "_m_" + datTime.strftime("%m") + "_y_" + datTime.strftime("%Y") + "_"

descriptor =  input("Please enter descriptor for this test (no special characters)")

dataIter = 1
dataName_base = "test_"
descriptorNS = descriptor.replace(' ', '_')
dataName = dataName_base + dat + descriptorNS + "_1"

exitStat = False

#FILE CREATION AND HEADERS
log = True
if log:
    while path.exists(dataName + ".txt"): #Check to see if our new file name is unique
        dataName = dataName_base + str(dataIter + 1) #If not unique incriment file name
        dataIter = dataIter + 1 #...Iter
    f = open(dataName+".txt", "w") #Create unique file
    f.write("test " + str(dataIter) + " Windsonic sensor\n")
    f.write("Descriptor, :" + descriptor + '\n')
    f.write("DATA FORMAT\n")
    f.write("Format, Wind Direction, Wind Speed, Units, Status, Checksum\n")



def log():
    while exit_thread.is_alive():
        #print(exit_thread.is_alive())
        if exitStat:
            f.close()
            time.sleep(1)
            sys.exit()
            break
        else:
            try:
                #Only log when switch is active
                newDat = ser.readline()
                newDat2 = newDat.replace(b"<STX>", b"")
                newDat3 = newDat.replace(b"<ETX>", b"")
                # byteChk = utf8len(newDat3)
                toWrite = str(time.time() - t0) + "," + str(newDat3)
                f.write(toWrite + "\n")
                sys.stdout.write(toWrite+"\r")
                sys.stdout.flush()
            except KeyboardInterrupt:
                print("Pressed Ctrl-C to terminate while statement")


def getExitStat():
    exitIn = input("Press 9 to terminate logging")
    if exitIn == "9":
        exitStat = True #Exit logging
        #exit_thread.join() #Kill thread


exit_thread = Thread(target=getExitStat)
exit_thread.daemon = True
log_thread = Thread(target=log)
log_thread.daemon = True

input("Serial connection established, press enter to begin logging")
t0 = time.time() #Get innitial time 
#DATA LOGGING SECTION
ser = serial.Serial('/dev/ttyUSB0', 38400)
exit_thread.start()
log_thread.start()


while log_thread.is_alive() and exit_thread.is_alive():
    time.sleep(0.1)

log_thread.join()
exit_thread.join()

#ENDGAME 
f.close()                  #⛔⛔⛔⛔ CLOSE FILE
