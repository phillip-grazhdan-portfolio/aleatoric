# Aleatoric

## Phillip Grazhdan

---
###### *Requires `scipy`, `numpy`, and `sounddevice`*

This program is an aleatoric music generator, it uses random chance to create a 
chord progression, song structure, and melody.

The way it works is:
- A key is chosen from A4-A5 (220-440Hz)
- A tempo is chosen from 80-160BPM
- A song structure is chosen (e.g. ABABCD)
- The program starts by choosing a chord progression for the given structure letter (I use the term "passage"). It will choose a new one for every new passage.
- The progression is parsed as such:
  - The string is separated into a list of the chord numerals
  - Each numeral is given to a function that matches the case, determines if the chord is minor, and returns a major or minor triad starting in the key given initially
- When the chord list for the passage is parsed, a numpy array is created and the sound data is stored within it
  - The tempo is calculated via `60/BPM`, and multiplied by 4 to indicate 4 beats per measure
  - Each note in a chord is calculated as a sawtooth via it's Fourier series, and each calculated note is summed together to form the triads
  - Each one measure chord playback is then appended to the full chord list.
- The melody is generated the same way, except there's only one dimension to concatenate, so no extra summing.

I'd say with how much longer this program took me to make, it is very nice to have the flexibility of Python's syntax
and how fun it is to mess it up sometimes (almost had my speakers blown out a few times).