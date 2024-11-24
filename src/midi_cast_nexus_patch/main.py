# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, TYPE_CHECKING                   # For annotating method signatures

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

    def __init__(self, id : str, bindings = List["MIDICastNexusBinding"], bpm : Union[str, int, None] = None, steps: Union[str, int, None] = None , repeat : Union[str, int, None] = None, nextPatch : Union[str, int, None] = None):
        self.id = id                # ID of the patch
        self.bpm = bpm              # BPM of the patch used to calculate gate with
        self.steps = steps          # Number of steps supported by patch (NONE means there is no maximum step that would reset the counter)
        self.repeat = repeat        # Number of types to repeat patch before going to another patch
        self.nextPatch = nextPatch  # What patch to go to next after repeating the patch a specificed number of times
        # No properties defined since they aren't intended to be directly accessed from the instance:
        self.bindings = bindings    # Bindings defined for patch
        self.nexus = None       # The nexus instance this patch is registered to
        self.currentStep = 1    # Step counter for patch

    ##############
    # Properties #
    ##############

    #----#
    # id #
    #----#

    @property
    def id(self):
        """GETTER for this patche's ID"""
        return self._id

    @id.setter
    def id(self, value : str):
        """SETTER fot this patch's ID"""
        self._id = value

    #-----#
    # bpm #
    #-----#

    @property
    def bpm(self):
        """GETTER for this patch's BPM"""
        return self._bpm

    @bpm.setter
    def bpm(self, value: Union[str, int, None]):
        """SETTER for this patch's BPM"""
        # NOTE: Setting NONE will default BPM to 120 
        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError(f"{value} is not a STRING of an INTEGER for setting a patch's BPM with!")
            self._bpm = int(value)
        elif isinstance(value, None):
            self._bpm = 120
        elif isinstance(value, int):
            self._bpm = value 
        else:
            raise ValueError(f"{value} is not a supported type for setting a patch's BPM  with!")
    
    #-------#
    # steps #
    #-------#

    @property
    def steps(self):
        """GETTER for number of steps this patch supports"""
        return self._steps
    
    @steps.setter
    def steps(self, value : Union[str, int, None]):
        """SETTER for number of steps tis patch supports"""
        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError(f"{value} is not a STRING of an INTEGER for setting a patch's number of steps with!")
            self._bpm = int(value)
        elif isinstance(value, None) or isinstance(value, int):
            self._bpm = value 
        else:
            raise ValueError(f"{value} is not a supported type for setting a patch's  number of steps  with!")


    ####################
    # Instance Methods #
    ####################

    def register(self, nexus: "MIDICastNexus"):
        """Sets nexus instance this patch belongs to and adds itself to patches manged by that instance"""
        self.nexus = nexus 
        nexus.registerPatch(self.id, self)

    def resetCurrentStep(self):
        """Reset current step by setting it to 1"""
        self.currentStep = 1

    def nextStep(self):
        """Increments current count stored by patch"""
        if self.steps is None:
            self.currentStep +=1 
        else:
            if self.currentStep + 1 > self.steps:
                self.resetCurrentStep()
            else:
                self.curentStep += 1

    def timePerStep(self):
        """Returns time per step calculated from set BPM of patch"""
        beatsPerSecond = self.bpm / 60 
        secondsPerBeat = 1 / beatsPerSecond
        timePerStep = secondsPerBeat / 4 # Time per quater note in seconds
        return timePerStep
    
    '''
    def calcGate(self, startStep : int, numberOfSteps : int, count : int = 1):
        """Calculates the gate per step for with optional count"""
        return ((startStep + numberOfSteps) * self.timePerStep()) / count 
    '''

    #################
    # Magic Methods #
    #################