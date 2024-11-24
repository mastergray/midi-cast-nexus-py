from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ResetEverything(MIDICastNexusControl):

    """Implent control for resetting everything..."""

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        print("Reseting everything...")
        self.nexus.isActive = False
        self.nexus.currentStep = 1
        self.nexus.currentTonic = None
        self.nexus.sendPanic()
        self.nexus.isActive = True
        print("Ready.")