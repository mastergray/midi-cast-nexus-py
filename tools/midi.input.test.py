# Dependencies
import mido # MIDI I/O Libraray 
import traceback   # For showing stack trace with an expcetion is raised

#########
# Setup #
#########

# List available input ports
input_ports = mido.get_input_names()
print("Available input ports:", input_ports)

# List available output ports
output_ports = mido.get_output_names()
print("Available output ports:", output_ports)

# TODO: Probably need better way of selecting ports:
inport = mido.open_input("E-MU XMidi1X1 Tab:E-MU XMidi1X1 Tab Out 20:0") 
outport = mido.open_output("E-MU XMidi1X1 Tab:E-MU XMidi1X1 Tab Out 20:0") 

########
# MAIN #
########

print("Listening....")
try:
    with inport:
        for msg in inport:  
            try:

                if msg.type == "control_change":
                    print(f"CONTROL CHANGE: {msg}")

                if msg.type == "program_change":
                    print(f"PROGRAM CHANGE: ${msg}")

                # Update step
                if msg.type == "note_on":
                    print(f"MESSAGE ON: {msg}")
                    
                if msg.type == "note_off":
                    print(f"MESSAGE OFF: {msg}")

                if msg.type == "pitchhweel":
                     print(f"PITCH WHEEL: {msg}")      
                                                      
            except Exception as err:
                print(err)  

except KeyboardInterrupt:
    inport.close()
    outport.close()

