from Resources.General import *

# -------- MORSE CODE -------- 
morseAlphabet = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..', }

def writeAsDotDashMorse( text, dot, dash, separator=' '):
    '''Translate a text from morse code with arbitrary characters into morse code with dots and dashes '''
    morseText = ''

    for ch in text:
        if ch == dot:
            morseText += '.'
        elif ch == dash:
            morseText += '-'
        else:
            morseText += separator

    return morseText

def Incrypt_Morse( plainText, morseKey=morseAlphabet, separator=' '):
    '''Incode a message encrypted with Morse code
    - Each character in morse code / the cipherText will be separated by a space (or separator character)
    '''   
    cipherText = ''
    for character in plainText:
        cipherText += morseKey[character] + separator
        
    return cipherText


def Decrypt_Morse( cipherText, morseKey=morseAlphabet, separator=' '):
    '''Decode a message encrypted with Morse code
    - Each character in morse code / the cipherText should be separated by a space (or separator character)
    '''
    morseKeyDecode = { v:k for k, v in morseAlphabet.items()}
    
    plainText = ''
    for character in cipherText.split(separator):
        plainText += morseKeyDecode[character]
        
    return plainText

# -------- MORSE CODE . -------- 
