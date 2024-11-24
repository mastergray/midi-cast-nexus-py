from midi_cast_nexus_control import MIDICastNexusControl
import mido

class TonicInput(MIDICastNexusControl):

    """Implements a control for updating the current tonic of the nexus instance it's registered to"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, msgChannel : int):
        super().__init__(msgChannel=msgChannel, msgType="note_on", msgValue=None)
        self.isActive = True
        self.isSwitched = False
        self.initChannel = msgChannel

    ####################
    # Instance Methods #
    ####################

    def toggle(self):
        """Toggle if tonic input is active or not"""
        self.isActive = not self.isActive
        msg = "Is Active" if self.isActive else "Is NOT Active"
        print(f"Tonic Input #{self.msgChannel} {msg}")

    def switch(self, fromChannel, toChannel):
        """Switches tonic input between a given channel and it's initialized channel"""
        if self.isSwitched is False and self.initChannel == fromChannel:
            print(f"Switch Tonic Input from #{self.msgChannel} to #{toChannel}")
            self.msgChannel = toChannel
            self.isSwitched = True
        else:
            if self.isSwitched is True and self.msgChannel == toChannel:
                print(f"Switch Tonic Input back from #{self.msgChannel} to #{self.initChannel}")
                self.msgChannel = self.initChannel 
                self.isSwitched = False
    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        if self.nexus.isActive is True and self.isActive is True:
           self.nexus.currentTonic = message.note
           print(f"Current Tonic: {TonicInput.MIDINoteName(message.note)}")

    #################
    # Magic Methods #
    #################

    def __str__(self):
        return f"Tonic Input: {self.msgChannel}"
    
    ##################
    # Static Methods #
    ##################

    @staticmethod 
    def MIDINoteName(midi_note):
        """Convert MIDI Note INT to note name"""
        if midi_note is None:
            return "None"
        # Note names for one octave
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        # Calculate the note name and octave
        note_name = note_names[midi_note % 12]
        octave = (midi_note // 12) - 1
        return f"{note_name}{octave}"