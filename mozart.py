from copy import deepcopy
from music21 import chord, note, scale, stream, instrument
import timeit
import os
import sys
import random
import math
from musicref import *

phraselength = 4

class Composer:
    def __init__(self, song=None, melodyTime=None):
        if not song:
            progression  = [None] * phraselength
            melody = []
            for time in melodyTime:
                melody.append([None, time])
            self.song = [melody, progression]
        else:
            self.song = song

    def melody(self):
        "The variable assignments for melody notes."
        return [s[0] for s in self.song[0]]

    def progression():
        "The variable assignments for chords."
        return list(self.song[1])

    def setMelodyNotePitch(self, number, pitch):
        "Setting the pitch of the note at the number."
        newSong = deepcopy(self.song)
        noteRes = note.Note(pitch, quarterLength=self.song[0][number][1])
        newSong[0][number][0] = noteRes
        return Composer(newSong, None)

    def setChord(self, number, chordpass):
        "Setting the chord at the number"
        newSong = deepcopy(self.song)
        chordRes = chord.Chord(keyVal[chordpass], quarterLength=4)
        newSong[1][number] = chordRes
        return Composer(newSong, None)

    def melodyComplete(self):
        "Checks if melody assignment breaks any rules"
        for notes in self.song[0]:
            if not notes[0]:
                return False
        return True

    def chordComplete(self):
        "Checks if melody assignment breaks any rules"
        for chords in self.song[1]:
            if not chords:
                return False
        return True

    def chordDomain(self, number):
        "Return domain for chord at number."
        available = [key for key in keyVal]
        impossible = []
        if number != 0:
            for i in range(number):
                for possibility in available:
                    if self.song[1][i]:
                        if set(self.song[1][i].normalOrder).isdisjoint(set(chord.Chord(keyVal[possibility]).normalOrder)):
                            impossible.append(possibility)
        b = [a for a in available if a not in impossible]
        random.shuffle(b)
        return b

    def melodyDomain(self, number):
        "Return pitch domain for melody note at number."
        time = 0
        for i in range(number):
            time += self.song[0][i][1]
        chordNum = math.floor(time/4)
        chords = self.song[1][chordNum]
        if chords.quality == 'minor':
            resScale = scale.MinorScale(chords.pitchNames[0])
            b = [str(p) for p in resScale.getPitches("C4", "C5")]
            random.shuffle(b)
            return b
        else:
            resScale = scale.MajorScale(chords.pitchNames[0])
            b = [str(p) for p in resScale.getPitches("C4", "C5")]
            random.shuffle(b)
            return b

    def generateChords(self):
        number = 0
        while number<len(self.song[1]):
            if not self.song[1][number]:
                break
            number += 1
        domain = self.chordDomain(number)
        possible = []
        for chords in domain:
            possible.append(self.setChord(number, chords))
        random.shuffle(possible)
        return possible

    def generateMelody(self):
        number = 0
        while number<len(self.song[0]):
            if not self.song[0][number][0]:
                break
            number += 1
        domain = self.melodyDomain(number)
        possible = []
        for pitches in domain:
            possible.append(self.setMelodyNotePitch(number, pitches))
        return possible

    def forwardCheckMelody(self):
        for number in range(len(self.song[0])):
            if not self.song[0][number][0] and len(self.melodyDomain(number)) == 0:
                return False
        return True

    def forwardCheckChords(self):
        for number in range(len(self.song[1])):
            if not self.song[1][number] and len(self.chordDomain(number)) == 0:
                return False
        return True

    def getMelodyWithForwardChecking(self):
        b = [s for s in self.generateMelody() if s.forwardCheckMelody()]
        random.shuffle(b)
        return b

    def getChordWithForwardChecking(self):
        b = [s for s in self.generateChords() if s.forwardCheckChords()]
        random.shuffle(b)
        return b

def generateMelodyTime():
    possibleLengths = [0.25, 0.5, 1, 1.5, 2, 3, 4]
    result = []
    total = 0
    while total < phraselength*4:
        cur = random.choice(possibleLengths)
        if total + cur <= phraselength*4:
            result.append(cur)
            total += cur
    return result


def solveMelodyCSP(problem):
    frontier = [problem]
    while frontier:
        state = frontier.pop()
        if state.melodyComplete():
            return state
        else:
            successors = state.getMelodyWithForwardChecking()
            frontier.extend(successors)
    return None

def solveChordCSP(problem):
    frontier = [problem]
    while frontier:
        state = frontier.pop()
        if state.chordComplete():
            return state
        else:
            successors = state.getChordWithForwardChecking()
            frontier.extend(successors)
    return None

def main():
    timeArr = generateMelodyTime()
    mozart = Composer(None, timeArr)
    solvedChord = solveChordCSP(mozart)
    solvedBoth = solveMelodyCSP(solvedChord)
    #print stuff out to music software
    composed = stream.Score()
    streamChord = stream.Part()
    for chord in solvedChord.song[1]:
        streamChord.append(chord)
    #streamChord.show()
    cl = instrument.Whistle()
    streamMelody = stream.Part()
    streamMelody.insert(0, cl)
    for note in solvedBoth.song[0]:
        streamMelody.append(note[0])
    #streamMelody.show()
    composed.append(streamChord)
    composed.append(streamMelody)
    composed.show()

if __name__ == '__main__':
    main()


