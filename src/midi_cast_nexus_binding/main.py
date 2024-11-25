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

class MIDICastNexusBinding(MIDICastNexusRelay):
    
    """Defines a MIDICastNexus "binding" that can send MIDI messages based on the current step and current tonic"""

    ###############
    # CONSTRUCTOR #
    ###############
    
    def __init__(self, msgChannel : Union[int, None], outputChannel : int, startStep : int, rate: int = 0, offset : int = 0, gate: Union[int, None] = None, count: int = 1):
        super().__init__(msgChannel=msgChannel, msgType="note_on")
        
        # NOTE: msgChannel determine which timeInput we are listening for message from
        self.outputChannel = outputChannel  # Where to send message to
        self.startStep = startStep          # When to send message
        self.rate = rate                    # How often to send messae (Defaults to 0 - meaning we are only matching aginst the start step)
        self.offset = offset                # Fine-tune by the given number of steps
        self.gate = gate                    # How long message is a active (NONE means notes will play until manually stopped)
        self.count = count                  # Number of message to send
        self.patch = None                   # Patch this binding is registered to 

    ########4############
    # Overriden Methods # 
    #####################

    # @Override
    def matchMessage(self, message : mido.Message) -> bool:
        currentStep = self.patch.nexus.currentStep
        if message.type == self.msgType:
            # NOTE: A msgChannel of NONE means a message from any time input will match this message:
            if self.msgChannel is None:
                if self.patch.nexus.isFromTimeInputChannel(message):
                    if self.rate == 0:
                        return currentStep == self.startStep
                    else:
                        return currentStep == self.startStep or (currentStep - self.offset) % self.rate == 0
                return False
            # NOTE: We subtract msgChannel by 1 since Mido treats channel 1 and channel 0:
            if hasattr(message, "channel") and self.msgChannel - 1 == message.outputChannel:
                return currentStep == self.startStep or (currentStep - self.offset) % self.rate == 0
        return False
