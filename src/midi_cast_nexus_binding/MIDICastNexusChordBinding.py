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

class MIDICastNexusChordBinding(MIDICastNexusBinding):

    """Defines binding for sending chords to a midi-cast-py server"""

    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, 
                 outputChannel: int, 
                 startStep : int, 
                 degrees : List[Union[str, int]], 
                 tonic: Union[str, None] = None,
                 transpose: Union[str, None] = None,
                 scale : Union[List[str], None] = None,
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
        
        # Instance Fields:
        self.degrees = degrees      # Chord tones
        self.tonic = tonic          # Default Tonic of chord (if NONE then chord will not send if tonicControl is NONE)
        self.transpose = transpose  # Degree to transpose chord by
        self.scale = scale          # Scale of chord (default to Major)
        self.velocity = velocity    # Velocity of the notes we are sending

    ####################
    # Instance Methods #
    ####################
    
    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        gateTime = self.patch.calcGateTime(self.gate, self.count)
        tonic = self.tonic if self.patch.nexus.currentTonic is None else self.patch.nexus.currentTonic
        if tonic is not None:
            for count in range(self.count):
                self.patch.nexus.sendChord(
                    channel=self.outputChannel, 
                    note=tonic,
                    degrees=self.degrees,
                    scale=self.scale,
                    transpose=self.transpose, 
                    gate=gateTime, 
                    velocity=self.velocity)    
      