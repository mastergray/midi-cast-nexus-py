from midi_cast_nexus_control import MIDICastNexusControl
import mido

class TimeInput(MIDICastNexusControl):

    """Implements a control for updating the step count of the nexus instance it's registered to"""

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
        """Toggle if Time INput is active or not"""
        self.isActive = not self.isActive
        msg = "Is Active" if self.isActive else "Is NOT Active"
        print(f"Time Input #{self.msgChannel} {msg}")

    def switch(self, fromChannel: int, toChannel: int):
        """Switches time input between a given channel and it's initialized channel"""
        if self.isSwitched is False and self.initChannel == fromChannel:
            print(f"Switch Time Input from #{self.msgChannel} to #{toChannel}")
            self.msgChannel = toChannel
            self.isSwitched = True
        else:
            if self.isSwitched is True and self.msgChannel == toChannel:
                print(f"Switch Time Input back from #{self.msgChannel} to #{self.initChannel}")
                self.msgChannel = self.initChannel 
                self.isSwitched = False
 
    # @Overide
    def onMatchedMessage(self, message: mido.Message) -> None:
        if self.nexus.isActive is True and self.isActive is True:
            # NONE means there are is no maximum step count to reset from:
            if self.nexus.steps is None:
                print(f"Current Step: {self.nexus.currentStep}")
            else :
                print(f"Current Step: ({self.nexus.currentStep} / {self.nexus.steps}")  
            if self.nexus.steps is None:
                self.nexus.currentStep += 1
            else:
                if self.nexus + 1 > self.nexus.steps:
                    self.nexus.currentStep = 1
                else:
                    self.nexus.currentStep +=1 

    #################
    # Magic Methods #
    #################

    def __str__(self):
        return f"Time Input: {self.msgChannel}"