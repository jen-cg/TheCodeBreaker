from Resources.General import *
from Resources.Caesar import *

# -------- VIGENERE SUBSTITUTION -------- 
def Incrypt_VigenereCipher( plainText, keyword, plainAlphabet=englishAlphabet ):
    
    # -------- Repeat / wrap the keyword along the length of the text
    repeatedKeyword = []
    for i in range(int(len(plainText) / len(keyword)) ):
        for j in range(len(keyword)):
            repeatedKeyword.append(keyword[j])  
    for i in range(len(plainText) % len(keyword)):
        repeatedKeyword.append(keyword[i])
    # -------- Repeat / wrap the keyword along the length of the text.

    # -------- Create a dictionary of the ordered plain alphabet 
    # This is needed in order to determine what shift to use
    order = {}
    for i, letter in enumerate(plainAlphabet):
        order[letter.upper()] = i
    # -------- Create a dictionary of the ordered plain alphabet.

    # -------- Incrypt the message
    cipherText = ''
    for i in range(len(plainText)):
        shift = int(order[repeatedKeyword[i]])
        cipherText += Incrypt_CaesarShiftCipher(plainText[i], -shift, plainAlphabet)
    # -------- Incrypt the message.

    return cipherText

def Decrypt_VigenereCipher( cipherText, keyword, plainAlphabet=englishAlphabet ):
    
    # -------- Repeat / wrap the keyword along the length of the text
    repeatedKeyword = []
    for i in range(int(len(cipherText) / len(keyword)) ):
        for j in range(len(keyword)):
            repeatedKeyword.append(keyword[j])  
    for i in range(len(cipherText) % len(keyword)):
        repeatedKeyword.append(keyword[i])
    # -------- Repeat / wrap the keyword along the length of the text.

    # -------- Create a dictionary of the ordered plain alphabet 
    # This is needed in order to determine what shift to use
    order = {}
    for i, letter in enumerate(plainAlphabet):
        order[letter.upper()] = i
    # -------- Create a dictionary of the ordered plain alphabet.

    # -------- Incrypt the message
    plainText = ''
    for i in range(len(cipherText)):
        shift = order[repeatedKeyword[i]]
        plainText += Decrypt_CaesarShiftCipher(cipherText[i], -shift, plainAlphabet)
    # -------- Incrypt the message.

    return plainText


def Break_VigenereChiSquared( cipherText, period, plainAlphabet=englishAlphabet, knownLetterFrequencies=letterFrequencies_English ):
    '''Break a Vigenere Cipher using Chi Squared Statistics
    - Period is the likely keyword length as determined via a Periodic IOC Calculation
    '''

    possibleShifts = [i for i in range(0, len(plainAlphabet))]

    order = {}
    for i, letter in enumerate(plainAlphabet):
        order[i] = letter.upper()

    keyword = ''
    for startPosition in range(period):

        # Extact a sequence of letters from the cipher text
        subText = [ cipherText[i] for i in range(startPosition,len(cipherText),period)]

        lowestScore = 1e99 # Any very high number
        incryptedShift = 0
        for shift in possibleShifts:
            # Test a possible decryption
            decryptedText_test = Decrypt_CaesarShiftCipher(subText, -shift, plainAlphabet)
            # Get Chi-Squared Score
            score = ChiSquaredStatistic(decryptedText_test, knownLetterFrequencies)
            # Update Solution
            if score < lowestScore:
                lowestScore = score
                incryptedShift = shift

        keyword += order[incryptedShift]
        
    return keyword, Decrypt_VigenereCipher(cipherText, keyword, plainAlphabet )


def Break_VigenereDictionarySearch(cipherText, period, plainAlphabet=englishAlphabet, dictionary=open('Resources/SampleTexts/commonEnglishWords.txt').readlines(), knownLetterFrequencies=letterFrequencies_English):
    '''Break a Vigenere Cipher by checking words from a dictionary
    - Period is the likely keyword length as determined via a Periodic IOC Calculation
    '''
    SelectWords = []
    for word in dictionary:
        word = word.strip()
        if len(word) == period:
            SelectWords.append(word)

    bestKey = []
    bestScore = 99e9
    for key in SelectWords:
        key = key.upper()
        decrypted = Decrypt_VigenereCipher(cipherText, key, plainAlphabet )
        score = ChiSquaredStatistic(decrypted, knownLetterFrequencies)
    if score < bestScore:
            bestKey = key
            bestScore = score
            
    return bestKey, Decrypt_VigenereCipher(cipherText,bestKey,plainAlphabet)

# -------- VIGENERE SUBSTITUTION. -------- 
