Executables: nEmulator.py, receiver.py, sender.py

To run nEmulator.py use the command:
  python nEmulator.py, with 9 parameters (in the exact order):
  - <emulator's receiving UDP port number in the forward (sender) direction>
  - <receiver’s network address>
  - <receiver’s receiving UDP port number>
  - <emulator's receiving UDP port number in the backward (receiver) direction>
  - <sender’s network address>
  - <sender’s receiving UDP port number>
  - <maximum delay of the link in units of millisecond>
  - <packet discard probability> (0 to 1)
  - <verbose-mode> (0 or 1)

To run receiver.py use the command:
  python receiver.py, with 4 parameters (in the exact order):
   - <hostname for the emulator>
   - <port number used by emulator to receive ACKS from the receiver>
   - <port number used by receiver to receive data from emulator>
   - <name of output file into which the data is written>

To run sender.py use the command:
  python sender.py, with 4 parameters (in the exact order):
   - <hostname for the emulator>
   - <port number used by emulator to receive data from the sender>
   - <port number used by sender to receive ARKs from the emulator>
   - <name of input file to be transferred>

NO manual compilations needed.

The programs should be able to run on any undergrad machines, namely:
- ubuntu1804-002.student.cs.uwaterloo.ca
- ubuntu1804-004.student.cs.uwaterloo.ca
- ubuntu1804-006.student.cs.uwaterloo.ca
