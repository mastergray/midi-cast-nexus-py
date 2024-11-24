from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ToggleTimeInput(MIDICastNexusControl):

    """Implent control for toggling time inputs by channel"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel, msgType, msgValue, timeChannel):
        super().__init__(msgChannel=msgChannel, msgType=msgType, msgValue=msgValue)
        self.timeChannel = timeChannel

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
       for timeInput in self.nexus.timeInput:
            if timeInput.msgChannel == self.timeChannel:
                timeInput.toggle()
      