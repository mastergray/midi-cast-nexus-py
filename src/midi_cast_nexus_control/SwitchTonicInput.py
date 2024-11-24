from midi_cast_nexus_control import MIDICastNexusControl
import mido

class SwitchTonicInput(MIDICastNexusControl):

    """Implents control for switching a tonic input from it's current channel to another channel and back"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel, msgType, msgValue, fromChannel, toChannel):
        super().__init__(msgChannel=msgChannel, msgType=msgType, msgValue=msgValue)
        self.fromChannel = fromChannel
        self.toChannel = toChannel

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
       for tonicInput in self.nexus.tonicInput:
            tonicInput.switch(self.fromChannel, self.toChannel)
      