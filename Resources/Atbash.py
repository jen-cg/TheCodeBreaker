from Resources.General import *

# -------- ATBASH -------- 
def Incrypt_Atbash(plainText, plainAlphabet=englishAlphabet):
    '''Atbash: The alphabet has been reversed
    - This is probably the simplest cipher
    '''
    
    cipherAlphabet = plainAlphabet[::-1]

    key = {}
    for i in range(len(plainAlphabet)):
        key[plainAlphabet[i].upper()] = cipherAlphabet[i].upper()

    cipherText = ''
    for character in plainText:
        if character.isalpha():
            cipherText = cipherText + key[character.upper()]
        else:
            cipherText = cipherText + character

    return cipherText


def Decrypt_Atbash(cipherText, plainAlphabet=englishAlphabet):
    '''Atbash: The alphabet has been reversed
    - This is probably the simplest cipher
    '''
    
    cipherAlphabet = plainAlphabet[::-1]

    key = {}
    for i in range(len(plainAlphabet)):
        key[cipherAlphabet[i].upper()] = plainAlphabet[i].upper()

    plainText = ''
    for character in cipherText:
        if character.isalpha():
            plainText = plainText + key[character.upper()]
        else:
            plainText = plainText + character

    return plainText


def Break_Atbash(cipherText, plainAlphabet=englishAlphabet):
    '''
    - Decrypt Atbash is equivalent to breaking Atbash
    '''
    return Decrypt_Atbash(cipherText, plainAlphabet=englishAlphabet)
# -------- ATBASH. -------- 