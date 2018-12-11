from copy import deepcopy
import timeit
import os
import sys
import random

def Composer:
	def __init__(self, melody):
		progression  = [None] * 4
        self.song = [melody, progression]

        # The values still remaining for a factor.
        self.factorRemaining = {}

        # The number of conflicts at a factor.
        self.factorNumConflicts = {}

        # For local search. Keep track of the factor state.
        if isFirstLocal:
            self._initLocalSearch()

    def melody(self):
    	"The variable assignments for melody notes."
    	return list(self.song[0])

    def progression():
    	"The variable assignments for chords."
    	return list(self.song[1])

    def setMelodyNotePitch(self, number, pitch):
    	"Setting the pitch of the note at the number."
    	newSong = deepcopy(self.song)
    	#21 syntax for adding pitch to a note object
    	newSong[0][number] = pitch

    def setChord(self, number, chord):
    	"Setting the chord at the number"
    	newSong = deepcopy(self.song)
    	#21 syntax
    	newSong[1][number] = chord

    def melodyComplete(self):
    	"Checks if melody assignment breaks any rules"
    	for note in self.song[0]:
    		if not note.pitch:
    			return False
    	return True

    def chordComplete(self):
		"Checks if melody assignment breaks any rules"
    	for chord in self.song[1]:
    		if not chord:
    			return False
    	return True

    def chordDomain(self, number):
    	"Return domain for chord at number."
    	available = set("all chords")
    	impossible = set()
    	for chord in self.song[1]:
    		for possibility in available:
    			#21 syntax
    			if not set.union(possibility triad, chord triad):
    				impossible.add(possibility)
    	return list(available - impossible)

    def melodyDomain(self, number):
    	"Return pitch domain for melody note at number."
    	time = sum(note.time for note before number)
    	chord = floor(time/4)
    	#syntax
    	return list("chord scale")

    def generateChords(self):
    	number = 0
    	while True:
    		if not self.song[1]
    			break
    		number += 1
    	domain = self.chordDomain(number)
    	possible = []
    	for chord in domain:
    		possible.append(self.setChord(number, chord))
    	return possible

    def generateMelody(self):
    	number = 0
    	while True:
    		#replace with music 21 syntax
    		if not self.song[0]
    			break
    		number += 1
    	domain = self.melodyDomain(number)
    	possible = []
    	for pitch in domain:
    		possible.append(self.setMelodyNotePitch(number, pitch))
    	return possible

    def forwardCheckMelody(self):
    	for number in range(len(self.song[0])):
    		if not self.song[0][number] and len(self.melodyDomain(number))
    			return False
    	return True

    def forwardCheckChords(self):
    	for number in range(len(self.song[1])):
    		if not self.song[1][number] and len(self.chordDomain(number))
    			return False
    	return True

    def getMelodyWithForwardChecking(self):
    	return [s for s in self.generateMelody() if s.forwardCheckMelody()]

    def getChordWithForwardChecking(self):
    	return [s for s in self.generateChords() if s.forwardCheckChords()]

def generateMelodyTime():
	possibleLengths = [0.25, 0.5, 1, 1.5, 2, 3, 4]
	result = []
	total = 0
	while total < 16:
		cur = random.choice(possibleLengths)
		if total + cur <= 16:
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
        if state.melodyComplete():
            return state
        else:
            successors = state.getChordWithForwardChecking()
            frontier.extend(successors)
    return None

def main():
	timeArr = generateMelodyTime()
	mozart = Composer(timeArr)
	solveMelodyCSP(mozart)
	solveChordCSP(mozart)
	print mozart.song
	#print stuff out to music softwrae?


if __name__ == '__main__':
	main()


