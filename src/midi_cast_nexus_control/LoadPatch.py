from midi_cast_nexus_control import MIDICastNexusControl
import mido

class LoadPatch(MIDICastNexusControl):

    """Implents control for loading in a patch by patch ID"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel, msgType, msgValue, patchID: str):
        super().__init__(msgChannel=msgChannel, msgType=msgType, msgValue=msgValue)
        self.patchID = patchID

    # @Override
    def onMatchedMessage(self, message: mido.Message) -> None:
        self.nexus.loadPatch(self.patchID)