from midi_cast_nexus_control import MIDICastNexusControl
import mido

class CCMapping(MIDICastNexusControl):

    """Implents control for mapping to some CC parameter of another device"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, 
                 outputChannel : int, 
                 from_cc : int,
                 to_cc : int, 
                 from_min : int = 0, 
                 from_max : int = 127, 
                 to_min = 0, 
                 to_max = 127):
        
        # Call parent constructor:
        super().__init__(msgChannel=None, msgType="control_change", msgValue=from_cc)

        # Instance Fields:
        self.outputChannel = outputChannel # Where to send CC value to 
        self.cc = to_cc                    # What CC param we are sending a value to
        self.from_min = from_min           # Minimum input value we are mapping from 
        self.from_max = from_max           # Maximum input value we are mapping from
        self.to_min = to_min               # Minimum output value we are mapping to   
        self.to_max = to_max               # Maximum output value we are mappng to             

    ####################
    # Instance Methods #
    ####################

    # @Override
    def onMatchedMessage(self, message: mido.Message) -> None:
        value = CCMapping.map_value(message.value, self.from_min, self.from_max, self.to_min, self.to_max)
        self.nexus.sendCC(channel=self.outputChannel, cc=self.cc, value=value)

     # @Override
    def matchMessage(self, message : mido.Message) -> bool:
        return message.type == self.msgType and message.control == self.msgValue

    ##################
    # Static Methods #
    ##################

    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        """Maps a single value from one range to another range using linear interpolation."""
        if in_min == in_max:
            raise ZeroDivisionError("Input range cannot have zero width (in_min == in_max).")
        # Map the value to the target range
        result = out_min + (out_max - out_min) * (x - in_min) / (in_max - in_min)
        # Round to the nearest integer and clamp to the target range
        return max(min(round(result), out_max), out_min)
