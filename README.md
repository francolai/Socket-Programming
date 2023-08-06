# Socket-Programming
A simulation of file transfer over the TCP protocol.

A file sender wants to send a file to a file receiver.
First, the file needs to be broken down into packets and send to the server.
The server has a chance to drop packets and receive packets late. It simulates the possibility of packet loss and latency in the real world.
The sender has to resend the packets that the server does not receive. Once all packets are received, the server sends the file to the receiver.
The receiver has to resemble the file with the packets received.
