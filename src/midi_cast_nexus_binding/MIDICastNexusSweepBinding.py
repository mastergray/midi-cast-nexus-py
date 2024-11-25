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

class MIDICastNexusSweepBinding(MIDICastNexusBinding):

    """Defines binding for sending a series of CC messages to a midi-cast-py server"""

    #################
    # Static Fielda #
    #################

    # Defines supported easing functions:
    # References from: https://easings.net/
    EASING = {
        "easeIn":[0.42, 0, 1.0, 1.0],
        "easeOut":[0, 0, 0.58, 1.0],
        "easeInOut":[0.42, 0, 0.58, 1.0],
        "linear":[0.0, 0.0, 1.0, 1.0],
        "easeInOutSine":[0.37, 0, 0.63, 1],
        "easeInSine":[0.12, 0, 0.39, 0],
        "easeOutSine":[0.61, 1, 0.88, 1],
        "easeInQuad":[0.11, 0, 0.5, 0],
        "easeOutQuad":[0.5, 1, 0.89, 1],
        "easeInOutQuad":[0.45, 0, 0.55, 1]
    }

    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, 
                 outputChannel: int, 
                 startStep : int, 
                 cc : int,
                 easing : str,
                 start:int = 0,
                 end: int = 127,
                 steps: int = 1,
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
        self.start = start # Starting value we are easing over
        self.end = end     # Ending value we are easing over
        self.steps = steps # Number of "steps" we are easing over (where gate is how long we are at with each step)
        self.value = MIDICastNexusSweepBinding.EASING.get(easing, None) # Easing function we are "sweeping" with

        # Throw an error if given easing function is not supported:
        if self.value is None:
            raise ValueError(f"{easing} is not a supported easing function!")

    ####################
    # Instance Methods #
    ####################
    
    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        gateTime = self.patch.calcGateTime(self.gate, self.count)
        for count in range(self.count):
            self.patch.nexus.sendSweepCC(channel=self.outputChannel, cc=self.cc, value=self.value, start=self.start, stop=self.end, steps=self.steps, gate=gateTime)
       