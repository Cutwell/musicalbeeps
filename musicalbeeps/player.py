#!/usr/bin/env python3

import time
import numpy as np
import simpleaudio as sa
import logging


class Player:
    def __init__(self, volume: float = 0.3, mute_output: bool = False):
        """ Initialize the player.

        :param volume: volume of the player (0.0 - 1.0)
        :param mute_output: mute output

        """

        if volume < 0 or volume > 1:
            raise ValueError("Volume must be a float between 0 and 1")

        # Frequencies for the lowest octave
        self.note_frequencies = {
            "A": 27.50000,
            "B": 30.86771,
            "C": 16.35160,
            "D": 18.35405,
            "E": 20.60172,
            "F": 21.82676,
            "G": 24.49971,
        }

        self.volume = volume
        self.mute_output = mute_output
        self.rate = 44100
        self.freq = 0
        self.fade = 800
        self._fade_in = np.arange(0.0, 1.0, 1 / self.fade)
        self._fade_out = np.arange(1.0, 0.0, -1 / self.fade)
        self._play_obj = None
        self._destructor_sleep = 0


    def __set_base_frequency(self, note: str):
        """Get base frequency for the note.

        :param note: note to play

        """

        letter = note[:1].upper()

        try:
            freq = self.note_frequencies[letter]

        except:
            raise Exception("Error: invalid note: '" + note[:1] + "'")

        return freq


    def __set_octave(self, freq, octave: str = "4"):
        """Set octave for the note.

        :param octave: octave to play the note

        """

        try:
            octaveValue = int(octave)

            if octaveValue < 0 or octaveValue > 8:
                raise ValueError("octave value error")

            freq *= 2**octaveValue

        except:
            raise Exception("Error: invalid octave: '" + octave + "'")

        return freq


    def __set_semitone(self, freq, symbol: str):
        """Set the semitone for the note.

        :param symbol: semitone to play the note

        """

        if symbol == "#":
            freq *= 2 ** (1.0 / 12.0)

        elif symbol == "b":
            freq /= 2 ** (1.0 / 12.0)

        else:
            raise Exception("Error: invalid symbol: '" + symbol + "'")

        return freq

    def __calc_frequency(self, note: str):
        """Calculate the frequency of the note.

        :param note: note to play

        """

        freq = self.__set_base_frequency(note)

        if len(note) == 1:
            freq = self.__set_octave(freq)

        elif len(note) == 2:

            if note[1:2] == "#" or note[1:2] == "b":
                freq = self.__set_octave(freq)
                freq = self.__set_semitone(freq, note[1:2])

            else:
                freq = self.__set_octave(freq, note[1:2])

        elif len(note) == 3:
            freq = self.__set_octave(freq, note[1:2])
            freq = self.__set_semitone(freq, note[2:3])

        else:
            raise Exception("Error: invalid note: '" + note + "'")

        return freq


    def __wait_for_prev_sound(self):
        """Wait for the previous sound to finish playing."""

        if self._play_obj is not None:
            while self._play_obj.is_playing():
                pass


    def __write_stream(self, freq, duration: float):
        """Write the stream to the output.

        :param duration: duration of the note

        """

        t = np.linspace(0, duration, int(duration * self.rate), False)

        audio = np.sin(freq * t * 2 * np.pi)
        audio = np.sign(audio)
        
        audio *= 32767 / np.max(np.abs(audio))
        audio *= self.volume

        if len(audio) > self.fade:
            audio[: self.fade] *= self._fade_in
            audio[-self.fade :] *= self._fade_out

        audio = audio.astype(np.int16)

        self.__wait_for_prev_sound()
        self._play_obj = sa.play_buffer(audio, 1, 2, self.rate)


    def __print_played_note(self, freq, note: str, duration: float):
        """Print the played note.

        :param note: note played
        :param duration: duration of the note

        """

        if self.mute_output:
            return

        if note == "pause":
            logging.info("Pausing for " + str(duration) + "s")

        else:
            logging.info(
                "Playing "
                + note
                + " ("
                + format(freq, ".2f")
                + " Hz) for "
                + str(duration)
                + "s"
            )


    def play_note(self, note: str, duration: float = 0.5):
        """Play a note.

        :param note: note to play
        :param duration: duration of the note

        """

        if note == "pause":
            self.__wait_for_prev_sound()
            self.__print_played_note(0, note, duration)
            time.sleep(duration)
            self._destructor_sleep = 0

        else:
            freq = self.__calc_frequency(note)

            self.__write_stream(freq, duration)
            self.__print_played_note(freq, note, duration)
            self._destructor_sleep = duration


    def get_audio(self, note: str, duration: float = 0.5):
        """ Convert note into audio (np array) without playing.
        
        :param note: note to play
        :param duration: duration of the note
        :return: np array of the note played for the duration

        """

        if note == "pause":
            # silence for the duration
            audio = np.zeros(((duration*44100)))

        else:
            freq = self.__calc_frequency(note)

            t = np.linspace(0, duration, int(duration * self.rate), False)

            audio = np.sin(freq * t * 2 * np.pi)
            audio = np.sign(audio)  # convert to square wave

            audio *= 32767 / np.max(np.abs(audio))
            audio *= self.volume

            if len(audio) > self.fade:
                audio[: self.fade] *= self._fade_in
                audio[-self.fade :] *= self._fade_out

            #audio = audio.astype(np.int16)

        return audio


    def __del__(self):
        """Wait for the previous sound to finish playing."""

        time.sleep(self._destructor_sleep)
