# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, Callable                    # For annotating method signatures
from midi_cast_nexus_control import MIDICastNexusControl    # Annotes a "control" in a method signature
from midi_cast_nexus_control import TimeInput               # For defining what inputs can control Nexus step counter
from midi_cast_nexus_control import TonicInput              # For defining what inputs can control Nexus tonic selector
from midi_cast_nexus_patch import MIDICastNexusPatch        # Annotes a "patch" in a method signature
import mido;                                                # MIDI I/O Framework
import requests                                             # For sending HTTP requests
import traceback                                            # For printing out stack trace from a caught exception

#########
# CLASS #
#########

class MIDICastNexus:

    """Implements patches and controls to improvise "music" with"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, url : str, timeInput : Union[int, List[int]], tonicInput : Union[int, List[int], None] = None, controls:Union[List[MIDICastNexusControl], None] = None, patches : Union[List[MIDICastNexusPatch], None] = None):
        self.url = url
        self.timeInput = timeInput 
        self.tonicInput = tonicInput
        self.controls = controls
        # State Variables:
        self.isActive = True     # Determine if messages can be relayed
        self.steps = None        # Number of steps in sequence
        self.currentStep = 1     # Current step of sequence
        self.currentTonic = None # Current tonic used by chords

    ##############
    # Properties #
    ##############

    #-----------#
    # timeInput #
    #-----------#

    @property
    def timeInput(self):
        """GETTER for time inputs registered to this instance"""
        return self._timeInput

    @timeInput.setter
    def timeInput(self, value: Union[int, List[int]]):
        """SETTER for registering time inputs to this instance"""
        self._timeInput = []
        if isinstance(value, list):
            for channel in value:
                self.registerTimeInput(channel)
        elif isinstance(value, int):
            self.registerTimeInput(value)
        else:
            pass

    #------------#
    # tonicInput #
    #------------#

    @property
    def tonicInput(self):
        """GETTER for tonic inputs registered to this instance"""
        return self._tonicInput
    
    @tonicInput.setter
    def tonicInput(self, value: Union[int, List[int], None]):
        """SETTER for registering time inputs to this instance"""
        self._tonicInput = []
        if isinstance(value, list):
            for channel in value:
                self.registerTonicInput(channel)
        elif isinstance(value, int):
             self.registerTonicInput(value)
        else:
            pass
    

    #----------#
    # controls #
    #----------#

    @property
    def controls(self):
        """GETTTER for controls registered to this instance"""
        return self._controls
    
    @controls.setter
    def controls(self, value):
        self._controls = []
        if isinstance(value, list):
            for control in value:
                if isinstance(control, MIDICastNexusControl):
                    self.registerControl(control)

    #---------#
    # patches #
    #---------#

    ####################
    # Instance Methods #
    ####################

    def registerTimeInput(self, channel: int):
        """Initalizes instance of timeInput using given channel and stores it in this nexus instance"""
        timeInput = TimeInput(msgChannel=channel)
        timeInput.nexus = self
        self._timeInput.append(timeInput)

    def registerTonicInput(self, channel: int):
        """Initalizes instance of tonicInput using given channel and stores it in this nexus instance"""
        tonicInput = TonicInput(msgChannel=channel)
        tonicInput.nexus = self
        self._tonicInput.append(tonicInput)

    def registerControl(self, control : MIDICastNexusControl):
        """Stores control in this nexus instance"""
        control.nexus = self 
        self._controls.append(control)
    
    def registerPatch(self, patch : MIDICastNexusPatch):
        """Adds patch to nexus"""
        pass 

    def loadPatch(self, id : str):
        """Set current patch of nexus"""
        pass

    '''
        HTTP Send Methods 
    '''

    def sendPanic(self):
        """Sends panic message to a midi-cast-py server"""
        url = f"{self.url}/panic"
        res = requests.get(url)        
        print("Panic: ", res.text)

    def sendNoteOn(self,  channel : int,  note: Union[int, str], gate : Union[int, float, None] = None, velocity : int = 127):
         """Send note on message for a specific channel of a midi-cast-py server"""
         url = f"{self.url}/on/{channel}"
         payload = {"note": note, "gate":gate, "velocity":velocity}
         print(payload)
         res = requests.post(url, json=payload)
         print("Note On: ", res.json())

    def sendNoteOff(self,  channel : int,  note: Union[int, str], gate : Union[int, float, None] = None, velocity : int = 127):
         """Send note on message for a specific channel of a midi-cast-py server"""
         url = f"{self.url}/off/{channel}"
         payload = {"note": note, "gate":gate, "velocity":velocity}
         res = requests.post(url, json=payload)
         print("Note Off: ", res.json())

    def sendNotes(self, channel : int, notes : List[str],  gate : Union[int, float, None] = None, velocity : int = 127):
        """Send message to play  multiple notes of a specific channel to midi-cast-py server"""
        url = f"{self.url}/notes/{channel}"
        payload = {"notes": notes, "gate":gate, "velocity":velocity}
        res = requests.post(url, json=payload)
        print("Notes: ", res.json())

    def sendChord(self, channel: int, note: int, degrees: List[str],  scale : Union[List[int], None] = None, transpose : str = None, gate : Union[int, float, None] = None, velocity : int = 127):
        """Send chord message for a specific channel of a midi-cast-py server"""
        url = f"{self.url}/chord/{channel}"
        payload = {"note":note, "degrees":degrees, "scale":scale, "transpose":transpose, "gate":gate, "velocity":velocity}
        res = requests.post(url, json=payload)
        print("Chord: ", res.json())

    def sendRest(self, channel : int , gate : Union[int, float, None] = None):
        """Sends stop message for a specific channel of a midi-cast-py-server"""
        url = f"{self.url}/stop/{channel}" 
        payload = {"gate":gate}
        res = requests.post(url, json=payload)
        print("Rest: ", res.json())

    def sendClear(self, channel:int):
        """Sends clear message for a specific of a midi-cast-py server"""
        url = f"{self.url}/clear/{channel}"
        res = requests.get(url)
        print("Clear: ", res.text)

    def sendCC(self, channel: int, cc : int, value : int, gate : Union[int, float, None] = None):
        """Send control message to specific channel of a midi-cast-py server"""
        url = f"{self.url}/cc/{channel}" 
        payload = {"cc":cc, "value":value, "gate":gate}
        res = requests.post(url, json=payload)
        print("CC: ", res.json())

    def sendSweepCC(self, channel : int, cc : int, value:List[int], start : int, stop : int, steps : int, gate : Union[int, float, None] = None):
        """Sends sweep CC message to specific channel of a midi-cast-py server"""
        url = f"{self.url}/cc/{channel}/sweep"
        payload = {"cc":cc, "value":value, "start":start, "stop":stop, "steps": steps, "gate":gate}
        res = requests.post(url, json=payload)
        print("Sweep CC: ", res.json())

    def sendXML(self, xml : str):
        """Sends midi-cast-py XML to midi-cast-py server"""
        url = f"{self.url}/xml"
        headers = {'Content-Type': 'application/xml'}
        res = requests.post(url, data=xml, headers=headers)
        print("XML: ", res.json())

    #################
    # Magic Methods #
    #################

    def __call__(self, inport : mido.ports.BaseInput) -> None:
        """Starts listening for MIDI messages from the given inport to relay to the set URL"""
        print("Started....")
        for timeInput in self.timeInput:
            print(timeInput)
        for tonicInput in self._tonicInput:
            print(tonicInput)
        try:
            with inport:
                for msg in inport:  
                    try:
                        for tonicInput in self.tonicInput:
                            tonicInput(msg)
                        for control in self.controls:
                            control(msg)
                        for timeInput in self.timeInput:
                            timeInput(msg)
                    except Exception as err:
                        print(err, msg)
                        traceback.print_exc()  
        except KeyboardInterrupt:
            print("Shutting down...")
            self.sendPanic()
            inport.close()


    ##################
    # Static Methods #
    ##################

    '''
    @staticmethod
    def setInt(value, invalidString: Callable[..., None], invalidType: Callable[..., None], ifNone: Union[int, Callable, None] = None):
        """Utility method for setting optional integer from a STRING"""
        if isinstance(value, str):
            if isinstance(value, str):
                if not value.isdigit():
                    errorMessage = invalidString(value)
                    raise ValueError(errorMessage)
                return int(value)
        elif isinstance(value, None):
            defaultValue = ifNone(value) if callable(ifNone) else ifNone
            if isinstance(defaultValue, Exception):
                raise defaultValue
            return defaultValue
        elif isinstance(value, int):
            return value
        else:
            errorMessage = invalidType(value)
            raise ValueError(errorMessage)
        
    @staticmethod
    def getMIDIMessageValue(message : mido.message):
        """Returns "value" of a MIDI message based on it's type"""
        if hasattr(message, "type"):
            if message.type in MIDICastNexus.msgTypes:
                if message.type == "note_on":
                    return message.note
                if message.type == "note_off":
                    return message.note
                if message.type == "pitchwheel":
                    return message.pitch
                if message.type == "control_change":
                    return 
            else:
                raise ValueError(f"{message.type} is not a supported MIDI message type!")
        else:
            raise ValueError("MIDI message does not have a set MIDI message type")
    '''

# Example usage
if __name__ == "__main__":

    from midi_cast_nexus_control import ResetEverything, SwitchTimeInput, SwitchTonicInput, ToggleTonicInput, ToggleActive

    # Define Controls:
    controls = [
        ResetEverything(msgChannel=10, msgType="note_on", msgValue=36),
        SwitchTimeInput(msgChannel=10, msgType="note_on", msgValue=37, fromChannel=4, toChannel=3),
        SwitchTonicInput(msgChannel=10, msgType="note_on", msgValue=38, fromChannel=3, toChannel=5),
        ToggleTonicInput(msgChannel=10, msgType="note_on", msgValue=39, tonicChannel=3)
    ]

    # TODO: Probably need better way of selecting ports:
    inport = mido.open_input("E-MU XMidi1X1 Tab:E-MU XMidi1X1 Tab Out 20:0") 

    # Initialize and start nexus:
    nexus = MIDICastNexus(url="http://127.0.0.1:5001", timeInput=[4, 5], tonicInput=3, controls=controls, patches=[])
    nexus(inport)