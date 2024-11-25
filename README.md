# midi-cast-nexus-py

For creating music with [midi-cast-py](https://github.com/mastergray/midi-cast-py/edit/main/README.md)

## Why "nexus" instead of "panel"?

Mainly to differentiate from [midi-cast-relay-panel](https://github.com/mastergray/midi-cast-relay-panel-py) and 
[midirig-py-v4](https://github.com/mastergray/midirig-py-v4) in the sense that approaching message relays has changed - instead of specify a specific range of steps to bind to, we now specify a starting step and some rate to repeat where "gate" is the number of steps to play that binding for. Further, with leveraging a "rate" to determine when something is played - this seems to better align with actual drumming (since we are leveage a modulus to determine how often something should be played given). This "cyclical" natue allows for much more intresting drum patterns, and so to reinforce this idea of building parts from cycles instead of sequences - the name was "nexus" was chosen. Also, I think it sounds cool - if not a little "mystical" - again to refinforce this idea of music as a cycle. As a series of repeating correspondences. As a ritual. As something to explore instead of something to merely construct. Or something like that, ig. 

## Setup 

1. Clone The Repo
>  git clone git@github.com:mastergray/midi-cast-py.git && cd midi-cast-py

2. Setup a virtual enviroment

> /usr/bin/python3.11 -m venv venv

3. Start the virtual enviroment

> source venv/bin/activate

4. Install dependencies

> pip install -r requirements.txt

### Notes

To create `requrements.txt`:

> pip freeze > requirements.txt



## TODO (11/24)

- Bindings
  - SweepBinding - see if we can make this work better
- JSON Config