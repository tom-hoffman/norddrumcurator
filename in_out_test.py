# simple interactive functional tests...

import functions
import mido

port_string = functions.getMidiPort()
print(f"Using port {port_string}") #doctest: +ELLIPSIS
p = mido.open_ioport(port_string)
functions.clearMidiMessages(p)
print("PROG DUMP ALL, please...")
all_mess = functions.receive_all(p)
rev = list(reversed(all_mess))
sending = []
for i in range(99):
    sending.append(functions.oneMessageToAll(rev[i], i))
p.close()
functions.send_all(sending)

    
    

    
    
