import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
import random

progressions = [
    "I-IV-ii-V",
    "I-vi-ii-V",
    "I-iii-IV-iv",
    "I-V-ii-V",
    "I-vi-IV-V",
    "IV-I-vi-IV",
    "I-V-vi-I",
    "I-IV-iv-I",
    "IV-V-I-I",
    "vi-IV-I-V"
]

structures = [
    "AABBCC",
    "ABABCD",
    "ABCDDD"
]

tonic = [
    220.00,
    246.94,
    261.63,
    293.66,
    329.63,
    349.29,
    392.00,
    440.00
]

def note_parse(key, numeral):
    note = key
    minor = False
    match numeral:
        case "ii":
            minor = True
            note *= pow(2, 2/12)
        case "iii":
            minor = True
        case "IV":
            note *= pow(2, 5/12)
        case "iv":
            minor = True
            note *= pow(2, 5/12)
        case "V":
            note *= pow(2, 7/12)
        case "vi":
            minor = True
            note *= pow(2, 9/12)
        case _:
            pass
    return note, minor

def relative_chord(given_note, numeral):
    note, minor = note_parse(given_note, numeral)
    if minor:
        return [note, note * pow(2, 3/12), note * pow(2, 7/12)]

    return [note, note * pow(2, 4/12), note * pow(2, 7/12)]

def parse(prog, key, tempo):
    chord_progression = []
    numeral_progression = prog.split("-")

    for i in numeral_progression:
        chord_progression += [relative_chord(key, i)]

    melody = [
    220.00, 246.94, 261.63, 293.66, 329.63, 349.29, 392.00, 440.00,
    220.00, 246.94, 261.63, 293.66, 329.63, 349.29, 392.00, 440.00,
    220.00, 246.94, 261.63, 293.66, 329.63, 349.29, 392.00, 440.00,
    220.00, 246.94, 261.63, 293.66, 329.63, 349.29, 392.00, 440.00 ]

    return chord_progression, melody

def build():

    key = random.choice(tonic)
    tempo = random.randint(80, 160)
    choose_structure = random.choice(structures)
    structure = list(choose_structure)
    chord_list = []
    melody_list = []
    chord_to_structure = {}

    print(structure)
    print("Tempo: ", tempo)

    for passage in structure:

        if passage not in chord_to_structure:
            chord_to_structure[passage] = random.choice(progressions)

        prog = chord_to_structure[passage]

        print (chord_to_structure) # dev

        chords, melody = parse(prog, key, tempo)

        for chord in chords:
            samplerate = 48000
            t = np.linspace(0.0, (60/tempo) * 4, int(samplerate * (60/tempo) * 4))
            chord_data = np.sum([-2/np.pi * np.sum([(pow(-1, k)) / k * np.sin(2 * np.pi * k * note * t) for k in range(1, 100)], axis=0) for note in chord], axis=0)
            chord_list.append(chord_data)

        combined_chord = np.concatenate(chord_list)

        # melody section needs to be implemented

    wav.write("ALEATORIC.wav", samplerate, combined_chord.astype(np.int16))

    sd.play(combined_chord, samplerate)
    sd.wait()

if __name__ == '__main__':
    build()