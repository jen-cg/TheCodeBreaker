from Resources.General import *

# -------- CLASSIC BACONIAN -------- 
AB_ClassicBaconianAlphabet = ['aaaaa', 'aaaab', 'aaaba', 'aaabb','aabaa', 'aabab', 'aabba', 'aabbb', 'abaaa','abaaa', 'abaab', 'ababa', 'ababb', 'abbaa', 'abbab', 'abbba', 'abbbb', 'baaaa', 'baaab', 'baaba', 'babbb', 'babbb', 'babaa', 'babab', 'babba', 'babbb']

def MakeClassicBaconianAlphabet(character1, character2):
    custom_BaconianAlphabet = []
    for item in AB_ClassicBaconianAlphabet:
        newItem = ''
        for character in list(item):
            if character == 'a':
                newItem += character1
            elif character == 'b':
                newItem += character2
        custom_BaconianAlphabet.append(newItem)          
    return custom_BaconianAlphabet


def Incrypt_ClassicBaconian(plainText,character1='a',character2='b', plainAlphabet=englishAlphabet):
    '''Before using this function, please remove all non-text characters (whitespace, punctuation, etc)
    '''
    BaconianAlphabet = MakeClassicBaconianAlphabet(str(character1), str(character2))
    
    key = {}
    for i in range(len(plainAlphabet)):
        key[plainAlphabet[i].upper()] = BaconianAlphabet[i].upper()

    cipherText = ''
    for character in plainText:
        if character.isalpha():
            cipherText = cipherText + key[character.upper()]
        else:
            cipherText = cipherText + character
            
    return cipherText


def Decrypt_ClassicBaconian(cipherText,character1='a',character2='b', plainAlphabet=englishAlphabet):
    '''Before using this function, please remove all non-text characters (whitespace, punctuation, etc)
    '''
    BaconianAlphabet = MakeClassicBaconianAlphabet(str(character1), str(character2))
    
    key = {}
    for i in range(len(plainAlphabet)):
        key[ BaconianAlphabet[i].upper()] = plainAlphabet[i].upper()

    plainText = ''
    for i in range(0,len(cipherText), 5):
        if cipherText[i:i+5] not in key.keys():
#             print('Error! This key does not work')
            return
        plainText += key[cipherText[i:i+5]]
      
    return plainText


def Break_ClassicBaconianCipher(cipherText,plainAlphabet=englishAlphabet):
    '''Before using this function, please remove all non-text characters (whitespace, punctuation, etc)
    '''
    character1, character2 = findAlphabet(cipherText)
    
    decryption_ab = Decrypt_ClassicBaconian(cipherText,character1,character2, plainAlphabet)
    if decryption_ab != 'None': 
        return decryption_ab
    decryption_ba = Decrypt_ClassicBaconian(cipherText,character2,character1, plainAlphabet)
    if decryption_ba != 'None': 
        return decryption_ba
# -------- CLASSIC BACONIAN. -------- 
