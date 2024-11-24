from midi_cast_nexus_control import MIDICastNexusControl
import mido

class SwitchTimeInput(MIDICastNexusControl):

    """Implents control for switching a time input from it's current channel to another channel and back"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel, msgType, msgValue, fromChannel, toChannel):
        super().__init__(msgChannel=msgChannel, msgType=msgType, msgValue=msgValue)
        self.fromChannel = fromChannel
        self.toChannel = toChannel

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
       for timeInput in self.nexus.timeInput:
            timeInput.switch(self.fromChannel, self.toChannel)
      