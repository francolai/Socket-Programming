from socket import *
from packet import *
import sys
import time
import random

def nEmulator(portforSender, recvAddr, recvPort, portforRecv, sendAddr,
              sendPort, maxDelay, discardProb, verbose_mode):
    maxDelay /= 1000
    # set up sockets for the sender
    socketforSender = socket(AF_INET, SOCK_DGRAM)
    socketforSender.bind(('', portforSender))
    # set up sockets for the receiver
    socketforRecv = socket(AF_INET, SOCK_DGRAM)
    socketforRecv.bind(('', portforRecv))
    socketforRecv.setblocking(False)
    
    while True:
        packet_sent = 0
        # receive packet from sender
        packetfromSender = packetDecode(socketforSender.recv(506))
        if verbose_mode:
            print("Receiving Packet {0}".format(packetfromSender.seqnum))
        # do not discard
        if random.random() >= discardProb or packetfromSender.type == EOT:
            # delay if it's not EOT packet
            if packetfromSender.type != EOT:
                delay = random.uniform(0, maxDelay)
                time.sleep(delay)
                socketforRecv.sendto(packetfromSender.encode(),
                                     (recvAddr, recvPort))                
                if verbose_mode:
                    print("Forwarding Packet {0}".
                          format(packetfromSender.seqnum))
            else:
                socketforRecv.sendto(packetfromSender.encode(),
                                     (recvAddr, recvPort))
                if verbose_mode:
                    print("EOT Packet from Sender is forwarding")
            packet_sent = 1
        else: # discard
            if verbose_mode:
                print("Discarding Packet {0}".format(packetfromSender.seqnum))
        
        # try to receive packet from receiver
        if packet_sent:
            time.sleep(0.01) # give receiver some time to send ACK
            packetfromRecv = packetDecode(socketforRecv.recv(506))
            if verbose_mode:
                print("Receiving ACK {0}".format(packetfromRecv.seqnum))            
            # do not discard
            if random.random() >= discardProb or packetfromRecv.type == EOT:
                # delay if it's not EOT packet
                if packetfromRecv.type != EOT:
                    delay = random.uniform(0, maxDelay)
                    time.sleep(delay)
                    socketforSender.sendto(packetfromRecv.encode(),
                                           (sendAddr, sendPort))
                    if verbose_mode:
                        print("Forwarding ACK {0}".
                              format(packetfromRecv.seqnum))            
                else:
                    socketforSender.sendto(packetfromRecv.encode(),
                                           (sendAddr, sendPort))
                    if verbose_mode:
                        print("EOT Packet from Receiver is forwarding")  
            else: # discard
                if verbose_mode:
                    print("Discarding ACK {0}".format(packetfromRecv.seqnum))           
        
if len(sys.argv) == 10:
    nEmulator(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),
              sys.argv[5], int(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), 
              int(sys.argv[9]))
   