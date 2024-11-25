from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ToggleMute(MIDICastNexusControl):

    """Implent control for muting output from a specific channel"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel, msgType, msgValue, muteChannel):
        super().__init__(msgChannel=msgChannel, msgType=msgType, msgValue=msgValue)
        self.muteChannel = muteChannel

    # @Override
    def onMatchedMessage(self, message: mido.Message) -> None:
        if self.muteChannel in self.nexus.mutedChannels:
            self.nexus.mutedChannels.remove(self.muteChannel)
            print(f"Unmuted #{self.muteChannel}")
        else:
             self.nexus.mutedChannels.append(self.muteChannel)
             self.nexus.sendClear(channel=self.muteChannel)
             print(f"Muted #{self.muteChannel}")