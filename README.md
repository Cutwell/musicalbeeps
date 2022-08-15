# musicalbeeps
[![GitHub](https://img.shields.io/github/license/Cutwell/musicalbeeps)](https://github.com/Cutwell/musicalbeeps/blob/master/LICENSE)

A python package to play sound beeps corresponding to musical notes. Extended to support layered melody and harmony for playing tunes made in the [Bitsy game editor](https://make.bitsy.org/).

This package uses the [numpy](https://pypi.org/project/numpy/) and [simpleaudio](https://pypi.org/project/simpleaudio/) packages.

## Install from source

```
$ git clone https://github.com/Cutwell/musicalbeeps
$ cd musicalbeeps
$ python setup.py install
```

## Usage

See `/test` for examples of playing songs with sequential notes (`/test/jukebox.py`) and songs with more complex layered melody and harmony (`/test/bitsy.py`)

### Initialization parameters for the `Player` class

|Name|Type|Default|Description|
|:---:|:---:|:---:|:---|
|`volume`|`float`|`0.3`|Set the volume. Must be between `0` and `1`|
|`mute_output`|`bool`|`False`|Mute the output displayed when a note is played|
