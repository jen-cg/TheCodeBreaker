from Resources.General import *

# -------- AFFINE SUBSTITUTION -------- 

def findAffineKeys(plainAlphabet = englishAlphabet):

    b = list(np.arange(0,len(plainAlphabet)))

    factorsAlphabetLength = findFactors(len(plainAlphabet))

    a = []
    for number in np.arange(1,len(plainAlphabet)):
        factorsNumber = findFactors(number)
        inBoth = [i for i in factorsNumber if i in factorsAlphabetLength and i !=1]
        if len(inBoth) == 0:
            a.append(number)

    return a, b

def Incrypt_Affine( plainText, a, b, plainAlphabet=englishAlphabet ):
    
    allowedA, allowedB = findAffineKeys(plainAlphabet)
    if a not in allowedA or b not in allowedB:
        print('Impermissible key')
        return None

    key = {}
    for p in range(len(plainAlphabet)):
        c = (a*p + 7)%len(plainAlphabet)
        key[plainAlphabet[p].upper()] = plainAlphabet[c].upper()

    cipherText = ''
    for character in plainText:
        if character.isalpha():
            cipherText = cipherText + key[character.upper()]
        else:
            cipherText = cipherText + character
            
    return cipherText


def Decrypt_Affine( cipherText, a, b, plainAlphabet=englishAlphabet ):
    
    allowedA, allowedB = findAffineKeys(plainAlphabet)
    if a not in allowedA or b not in allowedB:
        print('Impermissible key')
        return None


    key = {}
    for c in range(len(plainAlphabet)):
        a_invrt = pow(a,-1,len(plainAlphabet))
        p = a_invrt * (c-b) % len(plainAlphabet)
        key[plainAlphabet[c].upper()] = plainAlphabet[p].upper()

    plainText = ''
    for character in cipherText:
        if character.isalpha():
            plainText += key[character.upper()]
        else:
            plainText += character
            
    return plainText


def Break_Affine( cipherText, quadgramsFreq=quadgramFreq_English, plainAlphabet=englishAlphabet ):
    a, b = findAffineKeys(plainAlphabet)
    allKeys = [(int(x),int(y)) for x in a for y in b]
    
    bestKey = []
    bestScore = -99e9
    for key in allKeys:
        decryptTest = Decrypt_Affine(cipherText, key[0],key[1], plainAlphabet)
        score = quadgramFitness(decryptTest, quadgramsFreq)
        if score > bestScore:
            bestKey = key
            bestScore = score
    
    return bestKey, Decrypt_Affine(cipherText,bestKey[0],bestKey[1], plainAlphabet)
# -------- AFFINE SUBSTITUTION. -------- 
