# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, Callable    # For annotating method signatures
from abc import abstractmethod              # For documenting abstract methods
import mido                                 # Annotate MIDI message in a method signature

#########
# CLASS #
#########

class MIDICastNexusRelay:

    """Defines how to match against a MIDI message and what to do if that MIDI message is matched"""

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

    def __init__(self, msgChannel : Union[int, None], msgType:str):
        self.msgChannel = msgChannel 
        self.msgType = msgType

    ##############
    # Properties #
    ##############

    #------------#
    # msgChannel #
    #------------#

    @property
    def msgChannel(self):
        """SETTER for MIDI channel of message to match against"""
        return self._msgChannel
    
    @msgChannel.setter
    def msgChannel(self, value : Union[int, None]):
        """GETTER for MIDI channel of message to match against"""
        self._msgChannel = value

    #---------#
    # msgType #
    #---------#

    @property
    def msgType(self):
       """GETTER for MIDI message type to match against"""
       return self._msgType
    
    @msgType.setter 
    def msgType(self, value: str):
        """SETTER for MIDI message type to match against"""
        if value not in MIDICastNexusRelay.msgTypes:
            raise ValueError(f"{value} is not a supported MIDI message type!")
        self._msgType = value

    ####################
    # Abstract Methods #
    ####################

    @abstractmethod
    def matchMessage(self, message: mido.Message) -> bool:
        """Criteria to check against a MIDI message"""
        pass 

    @abstractmethod
    def onMatchedMessage(self, message: mido.Message) -> None:
        """What happens when we a message that meets criteria we are checking against"""
        pass
 
    #################
    # Magic Methods #
    #################

    def __call__(self, message : mido.Message) -> None:
        if self.matchMessage(message):
            self.onMatchedMessage(message)

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def getMIDIMessageValue(message : mido.Message) -> Union[int, tuple[int, int], None]:
        """Returns the value of a MIDI message based on type"""
        if message.type not in MIDICastNexusRelay.msgTypes:
            raise ValueError(f"{message.typ} is not a supported MIDI message type!")
        if message.type == "note_on" or message.type == "note_off":
            return message.note
        if message.type == "pitchwheel":
            return message.pitch 
        if message.type == "control_change":
            return (message.value, message.control)
        if message.type == "program_change":
            return message.program
        if message.type == "sysex":
            return message.data 
        return None