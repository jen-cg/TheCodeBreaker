import random
import numpy as np
from math import log10
import matplotlib.pyplot as plt
from math import gcd
import itertools


# -------- ENGLISH CHARACTERISTICS -------- 
englishAlphabet = list('abcdefghijklmnopqrstuvwxyz')

letterFrequencies_English = {'a':0.08167, 'b':0.01492, 'c':0.02782, 'd':0.04253, 'e':0.12702, 'f':0.02228, 'g':0.02015, 
                     'h':0.06094, 'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025, 'm':0.02406, 'n':0.06749, 
                     'o':0.07507, 'p':0.01929, 'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056, 'u':0.02758, 
                     'v':0.00978, 'w':0.02360, 'x':0.00150, 'y':0.01974, 'z':0.00074}
# -------- ENGLISH CHARACTERISTICS. -------- 


# -------- GENERAL FUNCTIONS -------- 
def prepareText(text):
    """
    This is a function to prepare a cipher text,
    written in alphabetic characters, for analysis.

    It does this by:
    1) removing all punctuation, whitespace, and nonalphabetic characters
    2) changing all alphabetic characters to upper case
    """

    preparedText = ''
    for item in list(text):
        if item.isalpha():
            preparedText = preparedText + item.upper()
    return preparedText


def removeCharacter( text , character):
    modifiedText = ''
    
    for item in list(text):
        if item != character:
            modifiedText = modifiedText + item
            
    return modifiedText


def reFormat(unformattedText, formattedText):
    '''
    Use this function to reformat a text after breaking the encryption 
    - formattedText is the original cipherText and unformattedText is
    the decrypted / broken cipher text
    '''
    unformattedText = list(unformattedText)
    reformattedText = ['']*len(formattedText)
    
    for i in range(len(formattedText)):
        character = formattedText[i]
        if character.isalpha():
            # Character is a letter
            if character.isupper():
                reformattedText[i] = unformattedText[i].upper()
            elif character.islower():
                reformattedText[i] = unformattedText[i].lower()
        else:
            # Character is whitespace or punctuation
            reformattedText[i] = formattedText[i]
            unformattedText.insert(i, character)
 
    return ''.join(reformattedText)


def findAlphabet(text):
    'Assumes all characters not in the alphabet (ie  white space and punctuation) has been removed'
    
    alphabet = []
    
    for character in text:
        if character not in alphabet:
            alphabet.append(character)
            
    return alphabet


def KeyWordAlphabet(keyword,placement, plainAlphabet=englishAlphabet):
    
    plainAlphabet = [ i.upper() for i in plainAlphabet ]
    keyword_norepeats = ''
    for i in keyword:
        i = i.upper()
        if i not in keyword_norepeats:
            keyword_norepeats = keyword_norepeats + i
            
    cipherAlphabet = ['0'] * len(plainAlphabet)
    remainingAlphabet = [i for i in plainAlphabet if i not in keyword_norepeats]

    # Place the end of the remaining alphabet at the begining of the cipher alphabet
    for i in range(placement):
        cipherAlphabet[i] = remainingAlphabet[len(plainAlphabet) - (placement + len(keyword_norepeats)):][i]

    # Place the keyword
    for j in range(len(keyword_norepeats)):
        cipherAlphabet[placement + j] = keyword_norepeats[j]

    # Fill the rest of the spots after the keyword with the reamaining alphabet
    for k in range(len(plainAlphabet) - (placement + len(keyword_norepeats))):
        cipherAlphabet[placement + len(keyword_norepeats) + k] = remainingAlphabet[k]
        
    return cipherAlphabet


def letterFrequencies( sampleText ):
    letterFrequencies_arbitraryLanguage = {}
    length_sampleText = 0

    for character in list(sampleText):

        if character.isspace() == False:
            length_sampleText = length_sampleText + 1

            if character.isalpha() == True:
                character = character.lower()

                if character in letterFrequencies_arbitraryLanguage.keys():
                    letterFrequencies_arbitraryLanguage[character] = letterFrequencies_arbitraryLanguage[character] + 1 
                else:
                     letterFrequencies_arbitraryLanguage[character] = 1

            else:
                if character in letterFrequencies_arbitraryLanguage.keys():
                    letterFrequencies_arbitraryLanguage[character] = letterFrequencies_arbitraryLanguage[character] + 1 
                else:
                     letterFrequencies_arbitraryLanguage[character] = 1

    for symbol in letterFrequencies_arbitraryLanguage.keys():
        letterFrequencies_arbitraryLanguage[symbol] = letterFrequencies_arbitraryLanguage[symbol]/length_sampleText

    return letterFrequencies_arbitraryLanguage


def ngramFrequencies(sampleText, n):
    '''
    Get the ngram frequencies of a given text 
        - ie n = 2 for bigram frequencies
        
    -Please remove all non-text characters before using
    '''

    ngramFreq = {}
    cnt = 0
    for i in range(len(sampleText) - n-1):
        cnt += 1
        ngram = ''.join([ c.upper() for c in list(sampleText[i:i + n]) ])
        
        if ngram in ngramFreq.keys():
             ngramFreq[ngram] += 1
        else:
            ngramFreq[ngram] = 1
    
    return { k: v / cnt for k, v  in sorted(ngramFreq.items(), key = lambda item: item[1], reverse=True) }


def IncidenceOfCoincidence(sampleText):
    """
    Please ensure that all characters a part of the text (no whitespace or punctuation)
    
    (There seem to be slighlty different ways of calculating IoC - so keep that in mind)
    """
    letterCounts = {}
    length_sampleText = len(sampleText)
    IoC = 0

    # Get counts of each letter
    for character in list(sampleText):
        character = character.lower()

        if character in letterCounts.keys():
            letterCounts[character] = letterCounts[character] + 1 
        else:
             letterCounts[character] = 1

    # Calculate the IoC
    for character in letterCounts.keys():
        IoC = IoC + letterCounts[character]*(letterCounts[character]-1)  
    IoC = IoC / ( length_sampleText*(length_sampleText-1) )
    
    return IoC


def periodicIOC(sampleText, longestLength=30):
    '''This function performs a periodic IOC calculation on the sample text
    '''
    # This considers the case of short sample texts 
    #   - we cannot do IOC on only 1 letter
    if longestLength > len(sampleText):
        longestLength = int(len(sampleText)/2)
    
    PeriodicIOC = {}
    for period in range(2, longestLength+1):
        IoC = []
        for startPosition in range(period):
            # Extact a sequence of letters from the cipher text
            subText = [ sampleText[i] for i in range(startPosition,len(sampleText),period)]
            IoC.append(IncidenceOfCoincidence(subText))
        PeriodicIOC[period] = np.mean(IoC)

    return PeriodicIOC


def ChiSquaredStatistic(sampleText, knownLetterFrequencies=letterFrequencies_English ):
    '''Compute the Chi-Squared Statistic for a sample text. 
    
    - A text that has letter frequencies more similar to the known 
    letter frequencies will get a lower score
    
    -Please remove all non-text characters  before calculatin the Chi-Squared Statistic
    '''
    textLength = len(sampleText)
    sampleLetterFrequencies = letterFrequencies(sampleText)
    
    ChiSquared = 0
    for letter in sampleLetterFrequencies.keys():
        expectedCount = knownLetterFrequencies[letter] * textLength
        actualCount = sampleLetterFrequencies[letter] * textLength
        
        ChiSquared += (actualCount - expectedCount)**2 / expectedCount
    return ChiSquared


def quadgramFrequencies_English():
    # Read the quadgram frequencies
    quadgramsFreq = {}
    quadgramsText = open('Resources/english_quadgrams.txt')
    quadgramsTextLines = quadgramsText.readlines()

    for quadgram in quadgramsTextLines:
        TextLine = quadgram.split(' ')
        quadgramsFreq[TextLine[0]] = int(TextLine[1][:-1])  # Lines end in \n character and we need to remove that

    quadgramsText.close()

    return quadgramsFreq

quadgramFreq_English = quadgramFrequencies_English()


def quadgramFitness(Text, quadgramsFreq=quadgramFreq_English):
    """
    Get the quadgram fitness for a text based on the given guadgram frequencies
    """
    totalQuadgrams = sum(quadgramsFreq.values())

    # For each quadgram in the cipherText, get the probablity of that quadgram occuring
    fitness = 0  # The measure of how close the text is to english
    for index in range(len(Text) - 3):
        if Text[index:index + 4] in quadgramsFreq.keys():
            probability = quadgramsFreq[Text[index:index + 4]] / totalQuadgrams
            logProb = log10(probability)
            fitness += logProb
        else:
            probability = 0.1 / totalQuadgrams
            logProb = log10(probability)
            fitness += logProb

    return fitness


class unknownCipher():
    def __init__(self, cipherText):
        """
        The first steps in cracking an unknown cipher

        Please make sure all puntucation and whitespace is removed and that all letters are in caps before using
            - See the removeCharacter function
        """
        
        self.lenText = len(cipherText)

        self.alphabet = findAlphabet(cipherText)
        
        self.numCharacters = len(self.alphabet)
        
        self.IOC = IncidenceOfCoincidence(cipherText)
        
        self.periodicIOC = periodicIOC(cipherText)
        
        self.letterFrequencies = letterFrequencies(cipherText)
        self.letterFreq = dict(sorted(self.letterFrequencies.items()))
        
        print('Number of Unique Characters  = {}'.format(self.numCharacters))
        print('Number of Characters in Text = {}'.format(self.lenText))
        
        print('\n')
        print('The Incidence of Coincidence = {:.3f}'.format(self.IOC))
        if  0.055 < self.IOC < 0.075:
            print('\t-The Incidence of Coincidence is similar to that of English (~0.066). The encryption method is likley to have been substitution')
        elif self.IOC <= 0.055:
            print('\t-The Incidence of Coincidence is less than that of English (~0.066). The encryption method is likley to have been polyalphabetic or polygraphic.')
              
            
        plt.figure(figsize=(10,4),dpi=120) 
        for i,key in enumerate(self.letterFreq):
            bar = plt.bar(i,self.letterFreq[key])
            if key in letterFrequencies_English.keys():
                plt.hlines(letterFrequencies_English[key], i-0.4, i+0.4, color='black',linewidth=2)

        xticks = plt.xticks(np.arange(len(self.letterFreq.keys())),self.letterFreq.keys())
        ylabel = plt.ylabel('Relative Frequency', fontsize=14)
        xlabel = plt.xlabel('CipherText Characters', fontsize=14)
        title = plt.title('Character Frequency of Ciphertext', fontsize=18)

        plt.figure(figsize=(10,4),dpi=120) 
        for i,key in enumerate(self.periodicIOC):
            bar = plt.bar(i,self.periodicIOC[key])
        xticks = plt.xticks(np.arange(len(self.periodicIOC.keys())),self.periodicIOC.keys())
        ylabel = plt.ylabel('Average IOC', fontsize=14)
        xlabel = plt.xlabel('Period', fontsize=14)
        title = plt.title('Periodic IOC Calculation', fontsize=18)
        
    def printLetterFrequencies(self,):
        print('\n')
        print('**LETTER FREQUENCIES**')
        print('Character  Frequency')
        print('--------------------')
        for item in self.letterFreq:
            print('{}\t     {:.3f}'.format(item.upper(),self.letterFreq[item]))
            print('--------------------')

    def printPeriodicIOC(self,):
        print('\n')
        print('**PERIODIC IOC CALCULATION**')
        print('Period      avg IOC')
        print('--------------------')
        for item in self.periodicIOC:
            print('{}\t     {:.3f}'.format(item,self.periodicIOC[item]))
            print('--------------------')

class wordCharacterization():
    def __init__(self, text, commonWordsPath='Resources/SampleTexts/commonEnglishWords.txt' ):
        '''
        Characterize the word usuage in a given text
        
        - If you have plain text from a given source you can use this to try to identify possible cribs to use 
        when breaking further messages from that source.  For example you may be able to identify an unsual word 
        the plain text author tends to use in their messages. 
        
        - Unusual words are defined to be any word not in the specified "commonWords" file
        '''
        
        # ----- Find all the word frequencies
        self.wordFreq = {} 
        for word in text.split():
            word = ''.join([ i.lower() for i in list(word) if i.isalpha() ])
            if word not in self.wordFreq.keys() and len(word) >0 :
                self.wordFreq[word] = 1
            elif len(word) >0 :
                self.wordFreq[word] += 1
        # Sort in decreasing order:
        self.wordFreq = {k: v for k, v in sorted(self.wordFreq.items(), key=lambda item: item[1], reverse=True)}
        # ----- Find all the word frequencies.

        # ----- Find unusual words
        commonWords = [ item.strip().lower() for item in open(commonWordsPath).readlines() ]

        self.unusualWords = {}
        for word in self.wordFreq.keys():
            if word not in commonWords:
                self.unusualWords[word] = self.wordFreq[word]
        # ----- Find unusual words

        print('Number of Words in Text = {}'.format(len(text.split())))
        print('Number of Unique Words  = {}'.format(len(self.wordFreq.keys())))
        
       
    def UnusualWords(self,):
        print('Number of Unusual Words  = {}'.format(len(self.unusualWords.keys())))
        print('\n')
        print('   **UNUSUAL WORDS**')
        print('Word              Count')
        print('-----------------------')
        for item in self.unusualWords:
            print('{:20}{}'.format(item,self.unusualWords[item]))
            print('-----------------------')
# -------- GENERAL FUNCTIONS. -------- 


def findFactors(x):
    '''A function to find all of the factors of a given number'''
    factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors