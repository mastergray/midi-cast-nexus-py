from midi_cast_nexus_control import MIDICastNexusControl
import mido

class SendPanic(MIDICastNexusControl):

    """Implent control for sending "panic" message for all MIDI devices"""

    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        self.nexus.sendPanic()
