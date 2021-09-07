#NIBP UN300C Serial port communication:
#The device is connected directly on Raspberry pi UART port

from struct import pack
import serial
import serial.tools.list_ports
import array

# Port initialization
serialInst = serial.Serial()
serialInst = serial.Serial("/dev/ttyS0", baudrate = 4800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)


#Read Serial Port
i=0
packet=""
packet2=""
packet3=""
serialInst.write("\x0201;;D7\x03".encode())
while i==0:
    
    if serialInst.in_waiting:    
          
        data = serialInst.read()
        if((data==b'\x02') or (data==b'\x03')):
            data=""
        if(data != b'\r'):
            packet +=str(data)
        #print(str((out*100)/samples)+'%')
        if(data == b'\r'):
            packet=packet.replace("'","")
            packet=packet.replace("b","")
            packet=packet.replace("C0S3","mmHg")
            #packet=packet.replace(";","\n")
            #packet=packet.replace("T","")
            #packet=packet.replace(" ","")
            #packet=packet.replace("S","\nSystem Status:")
            #packet=packet.replace(";A","\nPatient Mode:")
            #packet=packet.replace(";C","\nMeasurement Mode:")
            #packet=packet.replace(";M","\nError Information:")
            if (("S" in packet) and (";A" in packet) and (";C" in packet)):
                packet2 = packet.split(";")
                print(packet2)
                packet3 = list(packet2[4])
                print(packet3)
            else:
                print(packet)

            if(packet=="999"):
                print("Measurement Result:\n")
                serialInst.write("\x0218;;DF\x03".encode())
                
            packet=''
            
            