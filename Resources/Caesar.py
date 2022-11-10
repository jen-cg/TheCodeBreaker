from Resources.General import *

# -------- CAESAR SHIFT -------- 
def Incrypt_CaesarShiftCipher(plainText, shift, plainAlphabet=englishAlphabet):
    '''Caesar Cipher: The alphabet has been shifted a certain number of places'''
    cipherAlphabet = list(np.roll(plainAlphabet, shift))

    key = {}
    for i in range(len(plainAlphabet)):
        key[plainAlphabet[i].lower()] = cipherAlphabet[i].lower()
        key[plainAlphabet[i].upper()] = cipherAlphabet[i].upper()

    cipherText = ''

    for plainCharacter in plainText:

        # We will translate all letters from the plain alphabet into the cipher alphabet
        if plainCharacter.isalpha():
            cipherCharacter = key[plainCharacter]
            cipherText = cipherText + cipherCharacter

        # All other characters will just be copied over
        else:
            cipherText = cipherText + plainCharacter

    return cipherText


def Decrypt_CaesarShiftCipher(cipherText, shift, plainAlphabet=englishAlphabet):
    '''Caesar Cipher: The alphabet has been shifted a certain number of places'''
    cipherAlphabet = list(np.roll(plainAlphabet, shift))

    key = {}
    for i in range(len(plainAlphabet)):
        key[cipherAlphabet[i].lower()] = plainAlphabet[i].lower()
        key[cipherAlphabet[i].upper()] = plainAlphabet[i].upper()

    plainText = ''

    for cipherCharacter in cipherText:

        # We will translate all letters from the plain alphabet into the cipher alphabet
        if cipherCharacter.isalpha():
            plainCharacter = key[cipherCharacter]
            plainText = plainText + plainCharacter

        # All other characters will just be copied over
        else:
            plainText = plainText + cipherCharacter

    return plainText


def BreakCeasersCipher_singleLetterFrequecies(incryptedText, plainAlphabet=englishAlphabet, letterFrequencies_plainText=letterFrequencies_English):
    '''Caesar Cipher: The alphabet has been shifted a certain number of places'''
    
    possibleShifts = [i for i in range(1, len(plainAlphabet))] + [-i for i in range(1, len(plainAlphabet))]

    highestScore = 0
    decryptedText = ''
    incryptedShift = 0

    for shift in possibleShifts:
        score = 0

        # Test a possible decryption
        decryptedText_test = Decrypt_CaesarShiftCipher(incryptedText, shift, plainAlphabet)

        # Find Letter Frequency
        letterFrequencies_cipherText = {}
        for plainCharacter in plainAlphabet:
            cntr = 0
            for decryptedCharacter_test in list(decryptedText_test):
                if decryptedCharacter_test.lower() == plainCharacter:
                    cntr += 1
            letterFrequencies_cipherText[plainCharacter] = cntr

        # Calculate Score
        for character in plainAlphabet:
            score = score + letterFrequencies_cipherText[character] * (letterFrequencies_plainText[character] * 100)

        # Update Solution
        if score > highestScore:
            highestScore = score
            decryptedText = decryptedText_test
            incryptedShift = shift

    return incryptedShift, decryptedText


def BreakCeasersCipher_doubleLetterFrequecies(incryptedText, doubleLetterFrequencies, plainAlphabet=englishAlphabet):
    possibleShifts = [i for i in range(1, len(plainAlphabet))] + [-i for i in range(1, len(plainAlphabet))]

    highestScore = 0
    decryptedText = ''
    incryptedShift = 0

    for shift in possibleShifts:
        score = 0

        # Test a possible decryption
        decryptedText_test = Decrypt_CeaserShiftCipher(incryptedText, plainAlphabet, shift)

        # Find Double Letter Frequency
        doubleLetterFrequencies_cipherText = doubleLetterFrequencies(decryptedText_test, plainAlphabet)

        # Calculate Score
        for character in plainAlphabet:
            score = score + doubleLetterFrequencies_cipherText[character] * (
                        doubleLetterFrequencies[character] * 100)

        # Update Solution
        if score > highestScore:
            highestScore = score
            decryptedText = decryptedText_test
            incryptedShift = shift

    return incryptedShift, decryptedText
# -------- CAESAR SHIFT. -------- 
