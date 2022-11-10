from Resources.General import *

# -------- POLYBIUS SQUARE SUBSTITUTION CIPHER -------- 
def Incrypt_Polybius55(plainText,repeatCharacter1='i',repeatCharacter2='j', rowCharacters=['1', '2', '3', '4', '5'], columnCharacters=['1', '2', '3', '4', '5'], plainAlphabet=englishAlphabet):
    '''
    **Incrypt a 5x5 Polybius Square Cipher **
    
    Please remove all non-text characters before using 
    
    You can customize the incryption by changing the ordering of letters in 
    the plain alphabet, by changing the letters in the row and colum, or by 
    changing the characters which share the same encryption
    
    ex) 
    rowCharacters = ['A', 'B', 'C', 'D', 'E']
    columnCharacters = ['A', 'B', 'C', 'D', 'E']
    plainAlphabet = KeyWordAlphabet('Keyword',0)
    '''

    key = {}
    row =0
    column = 0
    for character in plainAlphabet:
        if character.upper() != repeatCharacter2.upper():
            key[character.upper()] = str(rowCharacters[row])+str(columnCharacters[column])
            if column < len(columnCharacters) -1:
                column = column + 1
            elif column == len(columnCharacters) -1:
                column = 0
                row = row + 1
    key[repeatCharacter2.upper()] = key[repeatCharacter1.upper()] 
    key = dict( sorted(key.items()) )

    cipherText = ''
    for plainCharacter in plainText:
        cipherCharacter = key[plainCharacter]
        cipherText += cipherCharacter


    return cipherText


def Incrypt_Polybius66(plainText, rowCharacters=['1', '2', '3', '4', '5', '6'], columnCharacters=['1', '2', '3', '4', '5', '6'], plainAlphabet=englishAlphabet):
    '''
    **Incrypt a 6x6 Polybius Square Cipher **
        
    Please remove all non-text characters before using 
    
    You can customize the incryption by changing the ordering of letters in 
    the plain alphabet or by changing the letters in the row and colum
    
    rowCharacters = ['A', 'B', 'C', 'D', 'E', 'F']
    columnCharacters = ['A', 'B', 'C', 'D', 'E', 'F']
    plainAlphabet = KeyWordAlphabet('Keyword',0)
    '''
    key = {}
    row =0
    column = 0
    for character in plainAlphabet+['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        key[character.upper()] = str(rowCharacters[row])+str(columnCharacters[column])
        if column < len(columnCharacters) -1:
            column = column + 1
        elif column == len(columnCharacters) -1:
            column = 0
            row = row + 1
      
    cipherText = ''
    for plainCharacter in plainText:
        cipherCharacter = key[plainCharacter]
        cipherText += cipherCharacter


    return cipherText


def Decrypt_Polybius55(cipherText,repeatCharacter1='i',repeatCharacter2='j', rowCharacters=['1', '2', '3', '4', '5'], columnCharacters=['1', '2', '3', '4', '5'], plainAlphabet=englishAlphabet):
    '''
    **Decrypt a 5x5 Polybius Square Cipher **
    
    Please remove all non-text characters before using 
    '''

    key = {}
    row =0
    column = 0
    for character in plainAlphabet:
        if character != repeatCharacter2:
            key[character.upper()] = str(rowCharacters[row])+str(columnCharacters[column])
            if column < len(columnCharacters) -1:
                column = column + 1
            elif column == len(columnCharacters) -1:
                column = 0
                row = row + 1
    key[repeatCharacter2.upper()] = key[repeatCharacter1.upper()] 
    key = dict( sorted(key.items()) )
    
    key = {v: k for k, v in key.items()}

    plainText = ''
    cipherText =  ''.join([c for c in cipherText if c.isspace() == False])
    for cipherCharacter in [ cipherText[i:i+2] for i in range(0, len(cipherText), 2) ]:
        plainCharacter = key[cipherCharacter]
        plainText += plainCharacter

    return plainText


def Decrypt_Polybius66(cipherText, rowCharacters=['1', '2', '3', '4', '5', '6'], columnCharacters=['1', '2', '3', '4', '5', '6'], plainAlphabet=englishAlphabet):
    '''
    **Decrypt a 6x6 Polybius Square Cipher **
        
    Please remove all non-text characters before using 
    '''

    key = {}
    row = 0
    column = 0
    for character in plainAlphabet+['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        key[character.upper()] = str(rowCharacters[row])+str(columnCharacters[column])
        if column < len(columnCharacters) -1:
            column = column + 1
        elif column == len(columnCharacters) -1:
            column = 0
            row = row + 1         
    key = {v: k for k, v in key.items()}
      
    plainText = ''
    cipherText =  ''.join([c for c in cipherText if c.isspace() == False])
    for cipherCharacter in [ cipherText[i:i+2] for i in range(0, len(cipherText), 2) ]:
        plainCharacter = key[cipherCharacter]
        plainText += plainCharacter

    return plainText


def Break_55Polybius(cipherText,quadgramsFreq=quadgramFrequencies_English(), plainAlphabet=englishAlphabet):
    '''
    **Break a 5x5 Polybius Square Cipher **
        
    Please remove all non-text characters before using 
    '''
    
    # Use the standard 5x5 Polybius key to get the message from double
    # letters to single  letters 
    cipherText = Decrypt_Polybius55(cipherText,plainAlphabet=plainAlphabet)
    
    # Break the substituion as a random sub cipher 
    Break_randomSubstitution(cipherText, quadgramsFreq=quadgramsFreq, plainAlphabet=plainAlphabet)
    
    
def Break_66Polybius(cipherText,quadgramsFreq=quadgramFrequencies_English(), plainAlphabet=englishAlphabet):
    '''
    **Break a 6x6 Polybius Square Cipher **
        
    Please remove all non-text characters before using 
    '''
    # Use the standard 6x6 Polybius key to get the message from double
    # letters to single  letters 
    cipherText = Decrypt_Polybius66(cipherText,plainAlphabet=plainAlphabet)

    # Break the substituion as a random sub cipher 
    Break_randomSubstitution(cipherText, quadgramsFreq=quadgramsFreq, plainAlphabet=plainAlphabet)
    
# -------- POLYBIUS SQUARE SUBSTITUTION CIPHER. -------- 
