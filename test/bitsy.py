# play tune using Bitsy note data

import musicalbeeps
import numpy as np
import logging
import time
import simpleaudio
import os


class SoundSystem:
    def __init__(self, verbose=False):
        self.audioContext = musicalbeeps.Player(volume=0.3, mute_output=not verbose)
        self.duration = 0.15  # duration of a single note

        self.barLength = 16
        self.minTuneLength = 1
        self.maxTuneLength = 16

        self.sampleRate = 44100

        self.l_balance, self.r_balance = 1, 1  # balance of left and right channels

        self.Note = {
            "NONE": -1,
            "C": 0,
            "C_SHARP": 1,
            "D": 2,
            "D_SHARP": 3,
            "E": 4,
            "F": 5,
            "F_SHARP": 6,
            "G": 7,
            "G_SHARP": 8,
            "A": 9,
            "A_SHARP": 10,
            "B": 11,
            "COUNT": 12,
        }

        self.ReversedNote = {
            -1: None,
            0: ("C"),
            1: ("C", "#"),
            2: ("D"),
            3: ("D", "#"),
            4: ("E"),
            5: ("F"),
            6: ("F", "#"),
            7: ("G"),
            8: ("G", "#"),
            9: ("A"),
            10: ("A", "#"),
            11: ("B"),
            12: "COUNT",
        }

        self.Solfa = {
            "NONE": -1,
            "D": 0,  # Do
            "R": 1,  # Re
            "M": 2,  # Mi
            "F": 3,  # Fa
            "S": 4,  # Sol
            "L": 5,  # La
            "T": 6,  # Ti
            "COUNT": 7,
        }

        self.Octave = {
            "NONE": -1,
            "2": 0,
            "3": 1,
            "4": 2,  # octave 4: middle C octave
            "5": 3,
            "COUNT": 4,
        }

        self.ReversedOctave = {-1: None, 0: "2", 1: "3", 2: "4", 3: "5", 4: "COUNT"}

        self.Tempo = {
            "SLW": 0,  # slow
            "MED": 1,  # medium
            "FST": 2,  # fast
            "XFST": 3,  # extra fast (aka turbo)
        }

        self.ReversedTempo = {0: "SLW", 1: "MED", 2: "FST", 3: "XFST"}

        self.SquareWave = {
            "P8": 0,  # pulse 1 / 8
            "P4": 1,  # pulse 1 / 4
            "P2": 2,  # pulse 1 / 2
            "COUNT": 3,
        }

        self.ArpeggioPattern = {
            "OFF": 0,
            "UP": 1,  # ascending triad chord
            "DWN": 2,  # descending triad chord
            "INT5": 3,  # 5 step interval
            "INT8": 4,  # 8 setp interval
        }

        # tempos are calculated as the duration of a 16th note in seconds
        # self.TempoScale = {
        #    "SLW": 0.250, # 60bpm (adagio)
        #    "MED": 0.1875, # ~80bpm (andante) [exact would be 187.5 ms]
        #    "FST": 0.125, # 120bpm (moderato)
        #    "XFST": 0.09375 # ~160bpm (allegro) [exact would be 93.75 ms]
        # }

        self.TempoScale = {
            "SLW": 250,  # 60bpm (adagio)
            "MED": 188,  # ~80bpm (andante) [exact would be 187.5 ms]
            "FST": 125,  # 120bpm (moderato)
            "XFST": 94,  # ~160bpm (allegro) [exact would be 93.75 ms]
        }

        self.ArpeggioScale = {
            "UP": [0, 2, 4, 7],
            "DWN": [7, 4, 2, 0],
            "INT5": [0, 4],
            "INT8": [0, 7],
        }

        # sawtooth waveform

    def tune(self, melody, harmony, tempo, key):
        """Play a tune with melody and harmony.

        :param melody: the melody to play
        :param harmony: the harmony to play
        :param tempo: the tempo to play the tune at
        :param key: the key to play the tune in

        :return: audio waveform data for tune

        """

        # convert tempo from ID to duration of a 16th note in seconds
        tempo = self.ReversedTempo[tempo]
        tempo = self.TempoScale[tempo]
        tempo /= 1000  # convert to milliseconds

        track = []

        for melody_bar, harmony_bar in zip(melody, harmony):
            # create empty audio of length barLength
            # 2 channels, 16 beats per bar, 44100 samples per second
            # samples per bar = time per beat * beats per bar * sample rate
            audio = np.zeros((int(tempo * self.barLength * self.sampleRate), 2))

            self.get_bar(audio, melody_bar, tempo)
            self.get_bar(audio, harmony_bar, tempo)

            # normalize to 16-bit range
            if np.max(np.abs(audio)) > 0:
                audio *= 32767 / np.max(np.abs(audio))

            # convert to 16-bit data
            audio = audio.astype(np.int16)

            # add bar to track
            track.append(audio)

        # concatenate bars
        track = np.concatenate(track)

        return track

    def play_track(self, track):
        """Play a track in a thread.

        :param track: the track to play

        """

        # play track
        play_obj = simpleaudio.play_buffer(track, 2, 2, self.sampleRate)

        # wait for playback to finish
        play_obj.wait_done()

    def get_bar(self, audio, bar, tempo):
        beatHead, beatTail = 0, 0

        for step in bar:
            # note and octave can have None values. Converting key to string means None values return 'None' key value
            note = self.ReversedNote[step["note"]]
            octave = self.ReversedOctave[step["octave"]]

            if len(note) > 1:
                note = note[0] + octave + note[1]
            else:
                note = note[0] + octave

            beats = step["beats"]

            if beats > 0:
                duration = beats * tempo

                # move beatHead to cover beats of this note
                beatHead += int(duration * self.sampleRate)

                # calculate note audio
                step_audio = self.audioContext.get_audio(note, duration)

                # add note audio to bar in left and right channels
                audio[beatTail:beatHead, 0] += self.l_balance * step_audio
                audio[beatTail:beatHead, 1] += self.r_balance * step_audio

                # move tail to head, and head by beats progressed
                beatTail = beatHead

    def beep(self, note, octave, beats):
        """PLay a single note.

        :param note: the note to play
        :param duration: the duration of the note

        """

        logging.debug(note, octave, beats)

        if len(note) > 1:
            note = note[0] + octave + note[1]
        else:
            note = note[0] + octave

        duration = beats * self.duration

        if duration > 0:
            self.audioContext.play_note(note, duration)
        else:
            # rest for beat duration
            time.sleep(self.duration)


if __name__ == "__main__":
    # set debug level to info
    logging.basicConfig(level=logging.INFO)

    import json

    # open resources/rhythmic_ruins.json
    with open(
        os.path.join(os.path.dirname(__file__), "resources", "rhythmic_ruins.json"), "r"
    ) as f:
        tune = json.load(f)

    audio = SoundSystem()

    song = tune["tune"]

    print(f"Playing {song['name']}")

    # calculate song waveform from tune
    track = audio.tune(song["melody"], song["harmony"], tempo=song["tempo"], key=song["key"])

    # play song
    audio.play_track(track)
