from socket import *
from packet import *
import sys
import time

DELAY = 0.2

def sender(emulator_addr, emulator_port, sender_port, inputFile):
    # create sender socket
    senderSocket = socket(AF_INET, SOCK_DGRAM)
    senderSocket.bind(('', sender_port))
    senderSocket.setblocking(False)
  
    # read data from file
    file = open(inputFile, "r")
    data = file.read()
    file.close()

    # prepare for log file
    seqlog = open("seqnum.log", "w")
    acklog = open("ack.log", "w")
    
    seqnum = 0
    listofpackets = []
    # no splitting of data if data size is less than 500 bytes.
    if len(data) <= 500:
        listofpackets.append(Packet(DATA, seqnum, len(data), data))
    # split data into multiple packets if data size is greater than 500 bytes.
    else:
        while len(data) > 500:
            listofpackets.append(Packet(DATA, seqnum, 500, data[0:500]))
            seqnum += 1
            data = data[500:]
        listofpackets.append(Packet(DATA, seqnum, len(data), data))
        
    # send data to emulator
    for i in range(len(listofpackets)):
        currPacket = listofpackets[i]
        senderSocket.sendto(currPacket.encode(), 
                            (emulator_addr, emulator_port))
        seqlog.write("{0}\n".format(currPacket.seqnum))
    # wait for 200ms
    time.sleep(DELAY)
    
    # receive ACKs from emulator, and retransmit if needed
    listofACK = []
    while len(listofACK) != len(listofpackets):
        for j in range(len(listofpackets)):
            try:  # try to obtain ACK packets
                ACKpacket = packetDecode(senderSocket.recv(506))
                ACKnum = ACKpacket.seqnum
                acklog.write("{0}\n".format(ACKnum))
                if ACKnum not in listofACK:
                    listofACK.append(ACKnum)
            except:
                break
        for k in range(len(listofpackets)):
            if k not in listofACK: # retransmit dropped packets
                senderSocket.sendto(listofpackets[k].encode(),
                                    (emulator_addr, emulator_port))
                seqlog.write("{0}\n".format(listofpackets[k].seqnum))
        time.sleep(DELAY)
        
    # send EOT:
    seqnum += 1
    senderSocket.sendto(Packet(EOT, seqnum, 0, "").encode(), 
                        (emulator_addr, emulator_port))
    seqlog.write("{0}\n".format(seqnum))
    
    # wait for EOT:
    while True:
        try:
            packet = packetDecode(senderSocket.recv(506))
            acklog.write("{0}\n".format(packet.seqnum))
            if packet.type == EOT:
                break
        except:
            continue
    seqlog.close()
    acklog.close()
    senderSocket.close()
    return

if len(sys.argv) == 5:
    sender(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])