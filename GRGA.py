# Guitar Riff Genetic Algorithm
# Patrick J Ropp | Propp@andrew.cmu.edu
# 11/30/2013
# Version 1.0

# This program details a potential genetic algorithm that constructs musically
# inclined sequences of notes to be played on the guitar, or guitar riffs. 

import math, random, sys, copy

#>>> Our Objects and Functions

# Initially we deal with 30 notes that construct the main region of the guitar
# fret board. These will be numbered 0-29, with 0 indicating the note E2 and
# 29 indicating A4. Each increment of a number indicates an increase of one
# semi-tone, i.e. E->F (0->1) or C->C# (8->9).
# (Notes from here on out will be indicated as their given absolute note
# numbers, or ANNs.)

ANNconv = ['E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb',
           'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb',
           'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb']

# The guitar has 6 strings tuned so that the 5th fret of one string is the same
# pitch as the open string directly adjacent to it. The one exception to this
# is the 3rd string whose adjacent string is tuned to its fourth fret.
# We hope to capture possible note combinations and to avoid attempting to play
# two notes on the same string. As such, we will only model with the notes that
# exist within the first four frets on each string, (with the exception of the
# 3rd string where we only go to the third fret.)

#>> Absolute Note Number to Tabulature Translator Function

# It should be noted here that the first string contains the highest notes, and
# subsequently higher strings contain subsequently lower notes. This is an
# unavoidable concequence of the traditional naming scheme. This simply means
# that when translating ANN to TAB we must start at the end of the list
# and move towards the front.
# TAB is mainly used for outputting readable note structures. We will only need
# it for performing output and checking that there are no string overlaps.

def ANNtoTAB(string, ANN):
    # We import two ints that will change to the appropriate numbers.
    string = 5
    # We reduce the ANN to a fret number for a given string.
    while ANN > 4:
        # We work backwards from the 6th string.
        string -= 1
        if string != 2:
            ANN -= 5
        else:
            ANN -= 4
    # Here we take the exception to the loop and manually change it.
    if ((ANN == 4) and (string == 2)):
        ANN = 0
        string = 1
    if ANN > 4:
        print "ERROR!!!"
    return [string,ANN]

#>> Chord Fitting Function

# For a given set of notes, we would like to give a number of potential chords
# that can be written. The length of such list is inversely proportional to
# the fitness of such notes, unless no chords can be found.
# We initially define all possible three note chords with their individual
# distances, and from pairwise distances we infer their relative root.
# For the major triad, whose distances are 0-4-7, we store the relative
# distances as 0,4,3 and 7 semi-tones. If a two note chord is 3 semi-tones
# apart, they could be part of the major triad located 4 semi-tones below the
# lowest note.

chordStruct = {'E':['E','Ab','B'],'Em':['E','G','B'],'F':['F','A','C'],
               'Fm':['F','Ab','C'],'Gb':['Gb','Bb','Db'],'Gbm':['Gb','A','Db'],
               'G':['G','B','D'],'Gm':['G','Bb','D'],'Ab':['Ab','C','Eb'],
               'Abm':['Ab','B','Eb'],'A':['A','Db','E'],'Am':['A','C','E'],
               'Bb':['Bb','D','F'],'Bbm':['Bb','Db','F'],'B':['B','Eb','Gb'],
               'Bm':['B','D','Gb'],'C':['C','E','G'],'Cm':['C','Eb','G'],
               'Db':['Db','F','Ab'],'Dbm':['Db','E','Ab'],'D':['D','Gb','A'],
               'Dm':['D','F','A'],'Eb':['Eb','G','Bb'],'Ebm':['Eb','Gb','Bb']}

# There can only be 1 or 0 chords for a 3 note chord. For a 2 note chord, there
# are a potential of 0 to 2 potential chords. For 1 note, all chords containing
# that note are considered, which totals at 15 different chords. 

def ChordFit(noteList):
    nameList = []
    for note in noteList:
        nameList.append(ANNconv[note])
    i = len(nameList)
    chordList = []
    """if (len(noteList) == 1):
        for key in chordStruct.keys():
            inChord = False
            if ((noteList[0] == chordStruct[key][0]) or
                (noteList[0] == chordStruct[key][1])):
                inChord = True
            if (inChord == True):
                chordList.append(key)
    else:"""
    if True:
        for key in chordStruct.keys():
            inChord = True
            for note in nameList:
                if note not in chordStruct[key]:
                    inChord = False
            if (inChord == True):
                chordList.append(key)
    return chordList


#>> Chord Object

# We would like to define a give chord by its TAB format. Each given string
# will have a default NULL value of -1, and a fret range of 0-4 (or 0-3 for
# string 3.) This will be the output value for printing results.
# We will also have a list of the ANNs for easy calculation,
# and a list of potential chord memberships.

class chord:
    def __init__(self, noteList=[]):
        self.valid = True
        self.noteList = noteList
        self.length = len(self.noteList)
        self.tabList = [-1,-1,-1,-1,-1,-1]
        self.chordList = []
        self.score = 0
        self.updateTAB()
        
    # We translate the ANNs to TAB to fill our empty TAB list
    def updateTAB(self):
        self.tabList = [-1,-1,-1,-1,-1,-1]
        #print self.noteList,'\t',
        for note in self.noteList:
            string = 0
            string = ANNtoTAB(string, note)
            if (string[1] > 4):
                print "ERROR: Invalid Notes"
            if (self.tabList[string[0]] == -1):
                self.tabList[string[0]] = string[1]
            else:
                self.noteList.remove(note)
        #print self.tabList
    
    # This will only output the notes in letter format for debugging purposes
    def __str__(self):        
        if (self.valid == False):
            return "ERROR: Invalid Chord"
        self.out = ""
        for note in self.noteList:
            self.out += ANNconv[note] + ','
        return self.out

    # This output function will output TAB frets for a specific string
    def str_out(self, string):
        self.updateTAB()
        if (self.tabList[string] > 4):
            print "ERROR: Invalid Notes"
        if (self.valid == False):
            print "X-",
        elif (self.tabList[string] == -1):
            print "--",
        else:    
            outstring = str(self.tabList[string])
            outstring += '-'
            print outstring,

    # We would like to have a function for generating new, completely random
    # sequences from scratch.
    def randomize(self):
        self.noteList = []
        self.tabList = [-1,-1,-1,-1,-1,-1]
        self.chordList = []
        self.score = 0
        length = random.randint(1,3)
        #print length,
        while (length > 0):
            newNote = random.randint(0,29)
            #print "[",newNote,"]"
            string = 0
            string = ANNtoTAB(string, newNote)
            if (self.tabList[string[0]] == -1):
                self.tabList[string[0]] = string[1]
                self.noteList.append(newNote)
                length -= 1
                #print length,
        #print
        self.length = len(self.noteList)

    # For the individual score of the chord we look at chord specificity.
    # The fewer number of possible chord participants, the better 'fit' and
    # so the higher score, for a maximum of 6.
    def score_self(self):
        self.chordList = ChordFit(self.noteList)
        if (len(self.chordList) == 0 ):
            self.score = -5
        else:
            self.score = 2*(6 - len(self.chordList))
        return self.score
    
    # For the purpose of scoring transitions, we would like to be able to
    # obtain the potential memberships that the chord contains. 
    def chords(self):
        return self.chordList

    # Mutations
    def mutate(self, percent):
        chance = random.randint(0,1000)
        if percent > chance:
            mute = random.randint(1,4)
            if (mute == 1) and (self.length < 3): #Insertion
                newNote = random.randint(0,29)
                stringNote = newNote
                string = 0
                ANNtoTAB(string, stringNote)
                if (self.tabList[string] == -1):
                    self.tabList[string] = newNote
                    self.noteList.append(newNote)
                self.length = len(self.noteList)
            if (mute == 2) and (self.length > 1): #Deletion
                out = random.randint(0,len(self.noteList)-1)
                self.noteList.pop(out)
                self.length = len(self.noteList)
                self.updateTAB()
            if (mute == 3):                       # Transition
                point = random.randint(0,len(self.noteList)-1)
                shift = random.randint(-1,1)
                note = self.noteList[point]
                note += shift
                if (note < 0):
                    note = 0
                if (note > 29):
                    note = 29
                self.noteList[point] = note
                self.updateTAB()
            if (mute == 4):                        # Chord Shift
                shift = random.randint(-1,1)
                for i in range(0,len(self.noteList)):
                    note = self.noteList[i]
                    note += shift
                    if (note < 0):
                        note = 0
                    if (note > 29):
                        note = 29
                    self.noteList[i] = note
                self.updateTAB()
                

#>> Riff Object
# Our Riff Object will contain a number of chords

class riff:
    def __init__(self, chordList=[]):
        self.chordList = chordList
        self.length = len(chordList)
        self.score = 0

    def str_out(self):
        for i in range(0,6):
            for chord in self.chordList:
                chord.str_out(i)
            print "\n"
        print self.score

    def score_self(self):
        self.score = 10 # This initialy 10 is to counter the -10 from not
                        # having a previous chord to compare
        prevChords = []
        for this in self.chordList:
            self.score += this.score_self()
            flag = False
            for prev in prevChords:
                for now in this.chords():
                    if chordStruct[now][0] in chordStruct[prev]:
                        flag = True
            prevChords = this.chords()
            if (flag == True):
                self.score += 10
            else:
                self.score -= 10
        return self.score

    def randomize(self):
        self.score = 0
        self.chordList = []
        limit = random.randint(3,10)
        for i in range(0,limit):
            new = chord()
            new.randomize()
            self.chordList.append(new)
        self.score_self()

    def mutate(self, percent):
        for chord in self.chordList:
            chord.mutate(percent)
            if (len(chord.noteList) == 0):
                self.chordList.remove(chord)
        chance = random.randint(0,1000)

    def splice(self, other):
        size = [len(self.chordList), len(other.chordList)]
        size.sort()
        mute = random.randint(3,size[0])
        newList = self.chordList[0:mute]
        newList += other.chordList[mute:]
        newriff = riff(newList)
        return newriff

    def shift(self):
        mute = random.randint(0,len(self.chordList))
        newList = self.chordList[mute:]
        newList += self.chordList[0:mute]
        self.chordList = newList


# From these definitions of riffs and chords, we will now construct our
# genetic algorithm. We will produce a population of riffs and from there
# we will shift for the top scoring riffs and then mutate the resulting
# population.

def sort(Pop, flag = False):
    top = Pop[0]
    bot = Pop[0]
    bad = Pop[0].score_self()
    score = Pop[0].score_self()
    for i in Pop:
        if i.score_self() > score:
            top = i
            score = top.score_self()
        elif i.score_self() < bad:
            bot = i
            bad = bot.score_self()
    total = 0
    if (flag == True):
        top.str_out()
        bot.str_out()
    for i in Pop:
        addition = (i.score_self() - bad)
        total += addition
    return [total, bad]

def topsift(Pop, old):
    top = old
    score = top.score_self()
    for i in Pop:
        if i.score_self() > score:
            top = i
            score = top.score_self
    return top

Population = []
for i in range(0,500):
    new = riff()
    new.randomize()
    Population.append(new)

best = riff()
best.randomize()
    
for i in range(0,101):
    print "[",i,"]"
    flag = False
    if (i%10 == 0):
        flag = True
    best = topsift(Population, best)
    split = sort(Population, flag)
    top = split[0] - 5
    bot = split[1]
    newPop = []
    for j in range(0,250):
        x = random.randint(0,top)
        point = -1
        while (x > 0):
            point += 1
            out = Population[point].score_self()
            x -= (out - bot)
        newCopy = copy.deepcopy(Population[point])
        newCopy.mutate((200-(2*i)))
        newPop.append(newCopy)
    for j in range(0,125):
        x = random.randint(0,top)
        y = random.randint(0,top)
        xpoint = -1
        ypoint = -1
        while (x > 0):
            xpoint += 1
            out = Population[xpoint].score_self()
            x -= (out - bot)
        while (y > 0):
            ypoint += 1
            out = Population[ypoint].score_self()
            y -= (out - bot)
        newCopy = Population[xpoint].splice(Population[ypoint])
        deeperCopy = copy.deepcopy(newCopy)
        newPop.append(deeperCopy)
    for j in range(0,125):
        x = random.randint(0,top)
        point = -1
        while (x > 0):
            point += 1
            if point > 500:
                point = 500
                x = -1
            out = Population[point].score_self()
            x -= (out - bot)
        newCopy = Population[point]
        deeperCopy = copy.deepcopy(newCopy)
        deeperCopy.shift()
        newPop.append(deeperCopy)
    Population = newPop

best.str_out()
for chord in best.chordList:
    print chord.chordList
