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
        
        if(data == b'\r'):
            packet=packet.replace("'","")
            packet=packet.replace("b","")
            packet=packet.replace("C0S3","mmHg")
            
            if (("S" in packet) and (";A" in packet) and (";C" in packet)):
                packet2 = packet.split(";")
                print(packet2[0].replace("S","System Status: "))
                print(packet2[1].replace("A","Patient Mode: "))
                print(packet2[2].replace("C","Measurement Mode: "))
                print(packet2[3].replace("M","Error Information: "))
                print(packet2[5].replace("R","Pulse Rate: ")+"bpm")
                packet3 = list(packet2[4])
                print("SYS: "+packet3[1]+packet3[2]+packet3[3]+"mmHg")
                print("DIA: "+packet3[4]+packet3[5]+packet3[6]+"mmHg")
                print("MEAN: "+packet3[7]+packet3[8]+packet3[9]+"mmHg")
            else:
                print(packet)

            if(packet=="999"):
                print("Measurement Result:\n")
                serialInst.write("\x0218;;DF\x03".encode())
                
            packet=''
            
            