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

class MIDICastNexusCCBinding(MIDICastNexusBinding):

    """Defines binding for sending CC messages to a midi-cast-py server"""

    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, 
                 outputChannel: int, 
                 startStep : int, 
                 cc : int,
                 value : Union[int, List[int]],
                 offset : int = 0,
                 timeInput : Union[int, None] = None, 
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
        
        self.cc = cc       # Which parameter we are sending the value to
        self.value = value # The value we are sending to the CC parameter


    ####################
    # Instance Methods #
    ####################
    
    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        gateTime = self.patch.calcGateTime(self.gate, self.count)
        for count in range(self.count):
            if isinstance(self.value, list):
                for value in self.value:
                    self.patch.nexus.sendCC(channel=self.outputChannel, cc=self.cc, value=value, gate=gateTime)
            else:
                self.patch.nexus.sendCC(channel=self.outputChannel, cc=self.cc, value=self.value, gate=gateTime)
       