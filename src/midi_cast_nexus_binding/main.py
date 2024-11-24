
# Dependencies:
from typing import Union, List, TYPE_CHECKING   # For annotating method signatures
from abc import abstractmethod                  # For documenting abstract methods
import mido                                     # Annotate MIDI message in a method signature

from midi_cast_nexus import MIDICastNexus   # Annotates a "nexus" instance in a method signature

# For preventing circular imports caused by type annotations:
if TYPE_CHECKING:
    from midi_cast_nexus_patch import MIDICastNexusPatch    # Annoates a "patch" instance in a method signature


#########
# CLASS #
#########

class MIDICastNexusBinding:

    """Defines how we can relay messages from a MIDI input to a MIDI output"""

    ################
    # Class Fields #
    ################

    # Supported messeage types:
    # NOTE: Message types are defined by Mido: https://mido.readthedocs.io/en/latest/message_types.html
    # NOTE: Not all message typs are currently supported:
    msgTypes = ["note_off", "note_on", "control_change", "program_change", "pitchwheel", "sysex", "clock", "start", "continue", "stop"]
    
    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, patch:MIDICastNexusPatch, msgType:str, msgChannel: Union[str, int, None]):
        self.patch = patch
        self.msgType = msgType 
        self.msgChannel = msgChannel

    ##############
    # Properties #
    ##############

    #-------#
    # patch #
    #-------#

    @property
    def patch(self):
        """GETTER for patch this binding is defined for"""
        return self._patch
    
    @patch.setter
    def nexus(self, value: MIDICastNexus):
        """SETTER for patch this binding is a defined for"""
        self._patch = value

    #---------#
    # msgType #
    #---------#

    @property
    def msgType(self):
        """GETTER for MIDI message type this binding is for"""
        return self._msgType
    
    @msgType.setter
    def msgType(self, value : str):
        """SETTER for MIDI message type this binding is for"""
        if value not in MIDICastNexusBinding.msgTypes:
             raise ValueError(f"{value} is not a supported MIDI message type!")
        self._msgType = value

    #------------#
    # msgChannel #
    #------------#

    @property
    def msgChannel(self):
        """GETTER for channel of MIDI message we are binding to"""
        return self._msgChannel
    
    @msgChannel.setter
    def msgChannel(self, value: List[str, int, None]):
        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError(f"{value} is not a STRING of an INTEGER for setting a MIDI channel with!")
            self._msgChannel = int(value)
        elif isinstance(value, None) or isinstance(value, int):
            self._msgChannel = value 
        else:
            raise ValueError(f"{value} is not a supported type for setting a MIDI channel with!")
        
    ###################
    # Abstact Methods #
    ###################

    @abstractmethod
    def onMessage(self, message : mido.Message):
        pass

    #################
    # Magic Methods #
    #################

    def __call__(self, message : mido.Message):
        """onMessage handler is called if MIDI message is of the right type and channel"""
        if message.type == self.msgType:
            if hasattr(message, "channel") is True and message.channel == self.msgChannel:
                self.onMessage(message)
            elif hasattr(message, "channel") is False and message.channel is None:
                self.onMessage(message)
            else:
                pass


    
    