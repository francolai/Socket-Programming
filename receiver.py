from socket import *
from packet import *
import sys
import time

def receiver(emulator_addr, emulator_port, receiver_port, outputFile):
    # create receiver socket
    receiverSocket = socket(AF_INET, SOCK_DGRAM)
    receiverSocket.bind(('', receiver_port))
    
    # prepare for log file
    arrlog = open("arrival.log", "w") 
    
    # receive packets and sends ACK/EOT accordingly
    listofpackets = []
    listofseqnum = []
    numPackets = -1
    while True:
        packet = packetDecode(receiverSocket.recv(506))
        seqnum = packet.seqnum
        arrlog.write("{0}\n".format(seqnum))
        if packet.type == DATA:
            ACK_packet = Packet(ACK, seqnum, 0, "")
            receiverSocket.sendto(ACK_packet.encode(),
                                  (emulator_addr, emulator_port))
            if seqnum not in listofseqnum:
                listofseqnum.append(seqnum)
                listofpackets.append(packet)
        elif packet.type == EOT:
            numPackets = seqnum

        # if an EOT packet is received and all data packets are received,
        # break loop
        if numPackets != -1 and len(listofseqnum) == numPackets:
            break
        
    # send EOT packet 
    EOT_packet = Packet(EOT, numPackets, 0, "")
    receiverSocket.sendto(EOT_packet.encode(),
                              (emulator_addr, emulator_port))
    
    # reorder packets
    listofpackets.sort(key=lambda x:x.seqnum)
    
    # write to outputFile
    file = open(outputFile, "w")
    for i in range(numPackets):
        file.write(listofpackets[i].data)
    file.close()
    
    arrlog.close()
    receiverSocket.close()
    return

if len(sys.argv) == 5:
    receiver(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])