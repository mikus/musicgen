import random

from music21 import *


beats_per_tact = 4
notes = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}
octave_distances = [2, 2, 1, 2, 2, 2, 1, 2]
repeats = 5
mash_chorus = True if not random.randrange(5) else False
note_note_chord = True if not random.randrange(3) else False
has_solo = True if not random.randrange(10) else False

base_beat_patterns = [
    [0,0,0,1],
    [0,0,1,2],
    [0,0,2,2,1,1,2,2],
    [0,1,2,0,1,1,0,0],
    [0,0,1,2,0,2,1,1],
    [0,1,2,1,0,2,2,1],
    [0,1,0,0],
    [0,0,0,0]
]

progressions = [
    [0, 3, 4, 4, 0, 3, 4, 0],
    [0, 3, 3, 0, 0, 4, 3, 0],
    [0, 3, 4, 4, 0, 5, 3, 4],
    [0, 6, 3, 4],
    [3, 4, 0],
    [0, 4, 0, 4, 0, 3, 0, 4],
    [0, 1, 4, 4],
    [1, 4, 0, 2],
    [1, 2, 3, 4, 4, 2, 1, 0],
    [0, 4, 6, 4],
    [5, 1, 4, 0]
]


def create_octave():
    base = random.randrange(12)
    octave = []
    for i in range(8):
        octave.append(notes[base])
        base += octave_distances[i]
        base = base % 12
    return octave


def get_chord(octave, base_note, chord_type=None, base_octave=5):
    if not chord_type:
        if base_note in [0,3,4]:
            chord_type = "major"
        else:
            chord_type = "minor"
    if chord_type == "major":
        interval_1 = 4
    else:
        interval_1 = 3
    interval_2 = 7
    note1 = note.Note(octave[base_note%8])
    octave_num = base_octave + int(base_note/8)
    note1.pitch.octave_num = octave_num
    for num, note_name in notes.items():
        if note1.name == note_name:
            note2 = note.Note(notes[(num+4)%12])
            octave_note2 = base_octave + int(num+interval_1/12)
            note3 = note.Note(notes[(num+7)%12])
            octave_note3 = base_octave + int(num+interval_2/12)
            break
    note2.pitch.octave_num = octave_note2
    note3.pitch.octave_num = octave_note3
    return chord.Chord([note1, note2, note3])


def generate_tact_beat(num):
    beats = ["16th", "eighth", "quarter", "half"]
    tact = []
    for i in range(beats_per_tact):
        choice = random.randrange(100)
       #if choice < 10:
       #    tact.append(beats[0])
       #    continue
        if choice < 25:#40:
            tact.append(beats[1])
            continue
        if choice < 100: #90:
            tact.append(beats[2])
            continue
        #if choice < 100:
        #    tact.append(beats[2])
        #    continue
    return tact


def generate_song_beat():
    tacts = []
    for i in range(3):
        tacts.append(generate_tact_beat(i))
    beat_pattern = random.choice(base_beat_patterns)
    print("beat pattern:", beat_pattern)
    song_beat = []
    for i in beat_pattern:
        song_beat.append(tacts[i])
    return song_beat


def generate_solo(octave, base_note):
    # Generate solo based on major chord, based on single note
    base_note = base_note % 7
    for num, name in notes.items():
        if name == octave[base_note]:
            note1 = notes[(num+4)%12]
            note2 = notes[(num+7)%12]
            base_num = num
            break
    else:
        print("FAIL")
    main_trinote = [octave[base_note], note1, note2]
    second_trinote = [note1, notes[(base_num+8)%12], notes[(base_num+11)%12]]
    third_trinote = [note2, notes[(base_num+11)%12], notes[(base_num+2)%12]]
    available_notes = main_trinote + second_trinote + third_trinote
    solo_length = 4 * random.randrange(4, 8)
    result = []
    while(solo_length):
        new_note = random.choice(available_notes)
        new_note = note.Note(new_note)
        result.append(new_note)
        result[-1].duration.type = "16th"
        solo_length -= 1
    return result


def generate(output):
    octave = create_octave()

    part = stream.Part()
    instruments = [
        instrument.Ocarina(),
        instrument.Guitar(),
        instrument.Harp(),
        instrument.Piano(),
        instrument.Woodblock(),
        instrument.BassTrombone()
    ]
    part.insert(0, random.choice(instruments))
    tempo = "4/{}".format(random.choice([1,2,3,4,5]))#, random.choice([1,2,3,4]))
    print("octave:", octave)
    print("tempo:", tempo)
    progression = random.choice(progressions)
    if progression == progressions[1]:
        tempo = "8/4"
    part.timeSignature = meter.TimeSignature(tempo)
    music = stream.Measure()
    beat = generate_song_beat()
    print("beat:")
    for b in beat:
        print("\t", b)
    base_ch = random.randrange(7)
    song_chords = []
    print("chord progression:", progression)
    print("base chord:", base_ch, "has solo:", has_solo, "mash_chorus:", mash_chorus, "note_chord:", note_note_chord)
    for ch in progression:
        song_chords.append(get_chord(octave, base_ch+ch))

    for repeat in range(repeats):
        for i, ch in enumerate(progression):
            for time in beat[i%len(beat)]:
                if mash_chorus and repeat in [2,4]:
                    this_chord = get_chord(octave, base_ch+ch, chord_type="major", base_octave=random.choice([1,2]))
                    this_chord.duration.type = "eighth" if random.randrange(2) else "quarter"
                    music.append(this_chord)
                elif has_solo and repeat == 3:
                    for solo_note in generate_solo(octave, base_ch):
                        music.append(solo_note)
                else:
                    this_chord = chord.Chord(song_chords[i%len(song_chords)])
                    this_chord.duration.type = time
                    if note_note_chord:
                        this_note = note.Note(octave[(base_ch+ch)%7])
                        this_note.duration.type = time
                        music.append(this_note)
                    music.append(this_chord)
    part.append(music)
    part.write("midi", fp=output)
