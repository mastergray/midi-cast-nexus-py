# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, Tuple, TYPE_CHECKING        # For annotating method signatures
import mido                                                 # Annotate MIDI message in a method signature
from midi_cast_nexus_binding import MIDICastNexusBinding    # Base class we are extending

# For preventing circular imports caused by type annotations:
if TYPE_CHECKING:
    from midi_cast_nexus import MIDICastNexus                   # Annotates a "nexus" instance in a method signature

#########
# CLASS #
#########

class MIDICastNexusSequenceBinding(MIDICastNexusBinding):

    """Defines binding for sending a sequence of notes to a midi-cast-py server"""

    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, 
                 outputChannel: int, 
                 startStep : int, 
                 notes: List[Union[str, int, List[str]]],
                 offset : int = 0,
                 timeInput : Union[int, None] = None, 
                 velocity: int = 127, 
                 rate: int = 0, 
                 gate: Union[int, None] = None, 
                 count: int = 1):
        
        # Call parent constructor:
        super().__init__(
            msgChannel=timeInput, 
            outputChannel=outputChannel, 
            startStep=startStep, 
            offset=offset,
            rate=rate, 
            gate=gate, 
            count=count)
        
        self.notes =  notes        # Notes that binding can send
        self.velocity = velocity   # Velocity of the notes we are sending


    ####################
    # Instance Methods #
    ####################
    
    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        gateTime = self.patch.calcGateTime(self.gate, self.count)
        for count in range(self.count):
            for note in self.notes:
                if note == "0" or note == 0:
                    self.patch.nexus.sendRest(self.outputChannel, gateTime)
                else:
                    notes = note if isinstance(note, list) else [note]
                    self.patch.nexus.sendNotes(channel=self.outputChannel, notes=notes, gate=gateTime, velocity=self.velocity)    
       