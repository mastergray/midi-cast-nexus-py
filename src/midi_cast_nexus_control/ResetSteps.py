from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ResetSteps(MIDICastNexusControl):

    """Implent control for resetting step counter"""

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        print("Reseting Steps...")
        self.nexus.currentStep = 1

