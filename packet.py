ACK = 0
DATA = 1
EOT = 2

class Packet:
    '''
    A class representing a packet
    '''
    def __init__(self, type, seqnum, length, data):
        self.type = type
        self.seqnum = seqnum
        self.length = length
        self.data = data
     
    # convert Packet into bytes object    
    def encode(self):
        type = str(self.type)
        seqnum = str(self.seqnum).zfill(2)
        length = str(self.length).zfill(3)
        return (type + seqnum + length + self.data).encode()

# convert bytes object back to Packet object.
def packetDecode(bytesObj):
    string = bytesObj.decode()
    type = int(string[0])
    seqnum = int(string[1:3])
    length = int(string[3:6])
    data = string[6:]
    return Packet(type, seqnum, length, data)