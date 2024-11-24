# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, Tuple, TYPE_CHECKING    # For annotating method signatures
import mido                                             # Annotate MIDI message in a method signature
from midi_cast_nexus_relay import MIDICastNexusRelay    # Base class we are extending

# For preventing circular imports caused by type annotations:
if TYPE_CHECKING:
    from midi_cast_nexus import MIDICastNexus                   # Annotates a "nexus" instance in a method signature

class MIDICastNexusControl(MIDICastNexusRelay):
    
    """Defines a MIDICastNexus "control" that can change the state of a nexus instance that control is registered to"""

    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, msgChannel : Union[int, None], msgType: str, msgValue : Union[int, tuple[int,int], None]):
        super().__init__(msgChannel, msgType)
        self.msgValue = msgValue 
        self.nexus = None

    ##############
    # Properties #
    ##############

    #----------#
    # msgValue #
    #----------#

    @property
    def msgValue(self):
        """GETTER for MIDI message value this control can operate on"""
        return self._msgValue
    
    @msgValue.setter 
    def msgValue(self, value :  Union[int, tuple[int,int], None]):
        """SETTER for MIDI message value this control can operate on"""
        self._msgValue =  value

    #-------#
    # nexus #
    #-------#

    @property
    def nexus(self):
        """GETTER for nexus instance this control is registered to"""
        return self._nexus
    
    @nexus.setter 
    def nexus(self, value : "MIDICastNexus"):
        """GETTER for nexus instance this control is registered to"""
        self._nexus = value

   ########4############
   # Overriden Methods # 
   #####################

    # @Override
    def matchMessage(self, message : mido.Message) -> bool:
        # NOTE: We subtract msgChannel by 1 since Mido treats channel 1 and channel 0:
        # NOTE: A message value of NONE means any value for this message is acceptable
        if message.type == self.msgType:
            if hasattr(message, "channel") is True and self.msgChannel - 1 == message.channel:
                return  self.msgValue is None or MIDICastNexusRelay.getMIDIMessageValue(message) == self.msgValue 
            if hasattr(message, "channel") is False and self.msgChannel is None:
                return self.msgValue is None or MIDICastNexusRelay.getMIDIMessageValue(message) == self.msgValue  
        return False


