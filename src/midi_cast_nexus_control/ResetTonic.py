from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ResetTonic(MIDICastNexusControl):

    """Implent control for reseting tonic"""

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        print("Reseting Tonic...")
        self.nexus.currentTonic = None
