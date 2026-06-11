import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="Outputs .wav file with specified name")
args = parser.parse_args()

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
            note *= pow(2, 4/12)
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

def relative_note(given_key, numeral):
    '''
    probability = [0.8, 0.2, 0.8, 0.2, 0.8, 0.2, 0.2, 0.8] # 80% chance for chord tone, otherwise 20%
    chosen_notes = random.choices([i * given_key / 220 for i in tonic], weights=probability, k=8)
    notes = []
    _, minor = note_parse(given_key, numeral)

    for note in chosen_notes:
        notes.append(note)

    return notes'''
    pass

def parse(prog, key):
    chord_progression = []
    numeral_progression = prog.split("-")
    melody = []

    for i in numeral_progression:
        chord_progression += [relative_chord(key, i)]
        # melody += relative_note(key, i)

    return chord_progression, melody

def build():

    key = random.choice(tonic)
    tempo = random.randint(80, 160)
    choose_structure = random.choice(structures)
    structure = list(choose_structure)
    chord_list = []
    melody_list = []
    chord_to_structure = {}
    combined_chord = []

    print(structure)
    print("Tempo: ", tempo)

    for passage in structure:

        if passage not in chord_to_structure:
            chord_to_structure[passage] = random.choice(progressions)

        prog = chord_to_structure[passage]

        print (chord_to_structure) # dev

        chords, melody = parse(prog, key)

        for chord in chords:
            samplerate = 48000
            t = np.linspace(0.0, (60/tempo) * 4, int(samplerate * (60/tempo) * 4))
            chord_data = np.sum([-2/np.pi * np.sum([(pow(-1, k)) / k * np.sin(2 * np.pi * k * note * t) for k in range(1, 100)], axis=0) for note in chord], axis=0)
            chord_list.append(chord_data)

        for note in melody:
            samplerate = 48000
            t = np.linspace(0.0, (60/tempo) * 0.5, int(samplerate * (60/tempo) * 0.5))
            melody_data = -2/np.pi * np.sum([(pow(-1, k)) / k * np.sin(2 * np.pi * k * note * t) for k in range(1, 100)], axis=0)
            melody_list.append(melody_data)

        combined_chord = np.concatenate(chord_list)
        # combined_melody = np.concatenate(melody_list)

        '''max_padding = max(len(combined_chord), len(combined_melody))

        if len(combined_chord) < max_padding:
            combined_chord = np.pad(combined_chord, (0, max_padding - len(combined_chord)))
        else:
            combined_melody = np.pad(combined_melody, (0, max_padding - len(combined_melody)))

        whole_song = combined_chord + combined_melody'''

    combined_chord /= np.max(np.abs(combined_chord)) * 2

    if args.output:
        wav.write(args.output, samplerate, (combined_chord * np.iinfo(np.int16).max).astype(np.int16))
    else:
        sd.play(combined_chord, samplerate)
        sd.wait()

if __name__ == '__main__':
    build()