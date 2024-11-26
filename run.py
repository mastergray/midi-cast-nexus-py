# Dependencies
import sys                                             # Getting command line arguments
import traceback                                       # For printing out stack trace from a caught exception
from src.midi_cast_nexus_json import MIDICastNexusJSON # For initializing and running an instance of MIDICastNexus from a JSON config

try:
    # Check if there are enough arguments from command line:
    if len(sys.argv) < 2:
        raise ValueError("No path given for JSON config")
    # Get arguments from command line:
    script_name, json_path = sys.argv
    # Initialize and run MIDICastNexus:
    MIDICastNexusJSON(json_path).start()
except Exception as e:
    print(e)  
    traceback.print_exc()  
    sys.exit(1)