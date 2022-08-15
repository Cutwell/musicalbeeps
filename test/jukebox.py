# test musicalbeeps module
import musicalbeeps as mb
import os

# create a player object
player = mb.Player(volume=0.3, mute_output=False)

# iterate songs in resources folder (assumes resources is in same directory as this file)
for song in os.listdir(os.path.join(os.path.dirname(__file__), 'resources')):
    print("Playing: " + song)

    # open song
    with open(os.path.join(os.path.dirname(__file__), 'resources', song), 'r') as f:
        # strip empty lines
        song = '\n'.join([line for line in f.read().split('\n') if line])

        # iterate notes
        for line in song.split('\n'):
            # split note and duration at :
            note, duration = line.split(':')

            # play note
            player.play_note(note, float(duration))
