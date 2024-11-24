from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ToggleTonicInput(MIDICastNexusControl):

    """Implent control for toggling tonic inputs by channel"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel, msgType, msgValue, tonicChannel):
        super().__init__(msgChannel=msgChannel, msgType=msgType, msgValue=msgValue)
        self.tonicChannel = tonicChannel

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
       for tonicInput in self.nexus.tonicInput:
            if tonicInput.msgChannel == self.tonicChannel:
                tonicInput.toggle()
      