# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from typing import Union, List, Any                # For annotating method signatures
import json                                             # For working with JSON 
import mido;                                            # MIDI I/O Framework
import importlib                                        # For dynamically loading in modules
import inspect                                          # For initialize classes from JSON
from midi_cast_nexus import MIDICastNexus               # For initializing an instance of nexus from the JSON config
from midi_cast_nexus_patch import MIDICastNexusPatch    # For initialing paches to register to an instance of nexus
import traceback                                        # For printing out stack trace from a caught exception

#########
# CLASS #
#########

class MIDICastNexusJSON:

    """For loading nexus config from JSON"""

    #################
    # Static Fields #
    #################

    # Defines binding types that can be registered to a patch:
    BINDING_TYPES = {
        "notes":"MIDICastNexusNoteBinding",
        "chord":"MIDICastNexusChordBinding",
        "rest":"MIDICastNexusRestBinding",
        "cc":"MIDICastNexusCCBinding",
        "seq":"MIDICastNexusSequenceBinding",
        "arp":"MIDICastNexusArpBinding"
    }

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, filename: str):
        try:
            with open(filename, 'r') as file:
                config = json.load(file)
            self.nexus = config 
            self.controls = config
            self.patches = config
            self.inport = config
            self.patchID = config
        except FileNotFoundError:
            raise Exception(f"The file was '{filename}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"The file `{filename}` contains invalid JSON.")

    ##############
    # Properties #
    ##############

    #-------#
    # nexus #
    #-------#

    @property
    def nexus(self):
        """GETTER for nexus instance we are initiazing from a JSON config"""
        return self._nexus
    
    @nexus.setter
    def nexus(self, value : dict):
        """SETTER for nexus instance we are initializing from a JSON config"""
        self._nexus = MIDICastNexusJSON.initClass(MIDICastNexus, value["settings"])

    @property
    def controls(self):
        """GETTER for controls to register the stored instance of nexus"""
        return self._controls
    
    @controls.setter
    def controls(self, value:dict):
        self._controls = []
        """SETTER for controls to register to the stored instance of nexus"""
        for controlArgs in value["controls"]:
            controlType = controlArgs["type"]
            control = MIDICastNexusJSON.loadControl(controlType, controlArgs)
            self._controls.append(control)

    #---------#
    # patches #
    #---------#

    @property 
    def patches(self):
        """GETTER for patches we can register to a stored nexus instance"""
        return self._patches 
    
    @patches.setter
    def patches(self, value: dict):
        """SETTER for patches we can register to thae nexure instance"""
        self._patches = []
        for patchID, patchArgs in value["patches"].items():
            patchArgs["id"] = patchID 
            for partID, part in patchArgs["parts"].items():
               # NOTE : "partID" is just a label to try and make the JSON easier to read since we can't use comments
               patchArgs["bindings"]  = self.initBindings(part, [])
            patch = MIDICastNexusJSON.initClass(MIDICastNexusPatch, patchArgs)
            self._patches.append(patch)
    
    #--------#
    # inport #
    #--------#

    @property
    def inport(self):
        """GETTER for MIDI device nexus can recieve messages from"""
        return self._inport
    
    @inport.setter 
    def inport(self, value : dict):
        """SETTER for MIDI device nexus can recieve message from"""
        deviceID = value["settings"]["deviceID"]
        self._inport = mido.open_input(deviceID) 

    #---------#
    # patchID #
    #---------#

    @property
    def patchID(self):
        """GETTER for ID of what patch to load first when nexus is started"""
        return self._patchID
    
    @patchID.setter
    def patchID(self, value: dict):
        """SETTER for ID of what patch to load first when nexus is started"""
        self._patchID = value["settings"]["patchID"]


    ####################
    # Instance Methods #
    ####################

    def start(self):
        """Starts nexus listening on loaded device"""
        self.nexus.controls = self.controls
        self.nexus.patches = self.patches
        self.nexus.loadPatch(self.patchID)
        self.nexus(self.inport)

    def initBindings(self, part : dict, result : list) -> list:
        """Initializes all bindings for a patch"""
        for bindingType in MIDICastNexusJSON.BINDING_TYPES.keys():
            self.initBinding(part, bindingType, result)
        return result

    def initBinding(self, part : dict, bindingType, result: list):
        """Initialize a binding for a specfic type from a config and stores in result"""
        if bindingType in part:
            for bindingArgs in part[bindingType]:
                bindingClass = MIDICastNexusJSON.BINDING_TYPES[bindingType]
                if bindingClass is None:
                    raise ValueError(f"{bindingType} is not a supported binding type")
                bindingArgs["outputChannel"] = part["outputChannel"]
                binding = MIDICastNexusJSON.loadBinding(bindingClass, bindingArgs)
                result.append(binding)
        
    ##################
    # Static Methods #
    ##################

    @staticmethod
    def loadClass(moduleName : str, className : str) -> type:
        """Loads the given class name from the given module name"""
        module = importlib.import_module(moduleName)
        return  getattr(module, className)
    
    @staticmethod
    def initClass(cls : type , json_data : dict) -> Any:

        """Initialize the given class with the given JSON data"""
        
        # Get constructor args from the given class:
        constructor_signature = inspect.signature(cls.__init__)
        constructor_args = constructor_signature.parameters
        
        # Get only constructor args from given JSON:
        args = {
            key: json_data[key]  # Include key-value pairs from json_data
            for key in constructor_args  # Iterate over all keys in constructor_params
            if key != "self" and key in json_data  # Only include keys valid for the constructor
        }

        # Initailize class and return instance: 
        return cls(**args)

    @staticmethod 
    def loadControl(controlName : str, args : Union[None, dict] = None):
        """Loads a MIDICastNexus "control" for the given control name"""
        # NOTE: Provding arguments as a dcitionary will try to return an instance of the class instead of the class itself
        cls = MIDICastNexusJSON.loadClass("midi_cast_nexus_control", controlName)
        return MIDICastNexusJSON.initClass(cls, args) if args is not None else cls
    
    @staticmethod 
    def loadBinding(bindingName:str, args : Union[None, dict] = None):
        """Loads a MIDICastNexus "binding" for the given control name"""
        # NOTE: Provding arguments as a dcitionary will try to return an instance of the class instead of the class itself
        cls = MIDICastNexusJSON.loadClass("midi_cast_nexus_binding", bindingName)
        return MIDICastNexusJSON.initClass(cls, args) if args is not None else cls

# Example usage
if __name__ == "__main__":
    try:
        filename = "./example.json"
        MIDICastNexusJSON(filename).start()
    except Exception as e:
        print(e)  
        traceback.print_exc()  