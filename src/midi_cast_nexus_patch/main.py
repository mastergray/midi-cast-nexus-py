# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, TYPE_CHECKING                   # For annotating method signatures
from midi_cast_nexus_binding import MIDICastNexusBinding        # For ensuring only bindings are registered to a patch
import mido

# For preventing circular imports caused by type annotations:
if TYPE_CHECKING:
    from midi_cast_nexus import MIDICastNexus                   # Annotates a "nexus" instance in a method signature
    from midi_cast_nexus_binding import MIDICastNexusBinding    # Annoates a "binding" instance in a method signautre

#########
# CLASS #
#########

class MIDICastNexusPatch:

    """Implements patches that can loaded and manged by MIDICastNexus"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, id : str, bindings = List["MIDICastNexusBinding"], bpm : Union[int, None] = 120, steps: Union[int, None] = None , repeat : Union[int, None] = None, nextPatch : Union[str, None] = None):
        self.id = id                # ID of the patch
        self.bpm = bpm              # BPM of the patch used to calculate gate with
        self.steps = steps          # Number of steps supported by patch (NONE means there is no maximum step that would reset the counter)
        self.repeat = repeat        # Number of types to repeat patch before going to another patch
        self.nextPatch = nextPatch  # What patch to go to next after repeating the patch a specificed number of times
        self.bindings = bindings    # Bindings defined for patch
        self.nexus = None           # The nexus instance this patch is registered to
        self.repeatCount = -1       # Number of times this patch has been played since it was loaded by nexus - we start at -1 to ensure that the patch has been repeated and not just played

    ##############
    # Properties #
    ##############

    #----------#
    # bindings #
    #----------#

    @property
    def bindings(self):
        """GETTER for bindings registered to this patch"""
        return self._bindings
    
    @bindings.setter
    def bindings(self, value):
        """SETTER for registering binding to this patch"""
        self._bindings = []
        if isinstance(value, list):
            for binding in value:
                if isinstance(binding, MIDICastNexusBinding):
                    self.registerBinding(binding)

    ####################
    # Instance Methods #
    ####################

    def registerBinding(self, binding:"MIDICastNexusBinding"):
        """Registers binding to this patch"""
        binding.patch = self 
        self._bindings.append(binding)

    def timePerStep(self):
        """Returns time per step calculated from set BPM of patch"""
        beatsPerSecond = self.bpm / 60 
        secondsPerBeat = 1 / beatsPerSecond
        timePerStep = secondsPerBeat / 4 # Time per quater note in seconds
        return timePerStep
    
    def calcGateTime(self, gate: Union[int, None], count : int):
        """Calculates the gate time in seconds"""
        if gate is None:
            return gate
        else:
            return (gate * self.timePerStep()) / count 
        
    def updateRepeat(self):
        """Determine if the patch has repeated or not"""
        if self.repeat is not None:
            if self.nexus.currentStep == self.steps:
                self.repeatCount += 1 
                print(f"{self.id} Repeated ({self.repeatCount} / {self.repeat})")

    #################
    # Magic Methods #
    #################

    def __call__(self, message : mido.Message):      
        # Checks if we need to load the next patch:
        if self.repeat is not None and self.repeatCount == self.repeat:
            if self.nextPatch is not None:
                self.nexus.loadPatch(self.nextPatch)
            else:
                self.nexus.loadPatch(None)
        else:
            # Otherwise call registed bindings:
            for binding in self.bindings:
                if binding.outputChannel not in self.nexus.mutedChannels:
                    binding(message)

