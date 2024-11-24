from midi_cast_nexus_control import MIDICastNexusControl
import mido

class ToggleActive(MIDICastNexusControl):

    """Toggles if nexus instance is active or not"""

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        self.nexus.isActive = not self.nexus.isActive
        msg = "Is Active" if self.nexus.isActive else "Is Not Active"
        print(f"Nexus {msg}")
