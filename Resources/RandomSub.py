from Resources.General import *

# -------- RANDOM SUBSTITUTION -------- 
def Incrypt_RandomSubCipher(plainText, plainAlphabet=englishAlphabet):
    cipherAlphabet = plainAlphabet.copy()
    random.shuffle(cipherAlphabet)

    key = {}
    for i in range(len(plainAlphabet)):
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

    return cipherText, cipherAlphabet


def Decrypt_RandomSubCipher(cipherText, cipherAlphabet, plainAlphabet=englishAlphabet):
    key = {}
    for i in range(len(plainAlphabet)):
        key[cipherAlphabet[i].upper()] = plainAlphabet[i].upper()

    plainText = ''

    for cipherCharacter in cipherText:

        # We will translate all letters from the plain alphabet into the cipher alphabet
        if cipherCharacter.isalpha():
            plainCharacter = key[cipherCharacter.upper()]
            plainText = plainText + plainCharacter

        # All other characters will just be copied over
        else:
            plainText = plainText + cipherCharacter

    return plainText


def Break_randomSubstitution(cipherText, quadgramsFreq=quadgramFreq_English, plainAlphabet=englishAlphabet):
    maxAlphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    maxScore = -99e9
    parentScore, parentAlphabet = maxScore, maxAlphabet[:]

    # Each 'realization' is a different random starting alphabet
    for realization in range(5):

        # Randomly shuffle the alphabet
        random.shuffle(parentAlphabet)

        # Decipher the ciperText using the parent alphabet
        parentDeciphered = Decrypt_RandomSubCipher(cipherText, plainAlphabet, parentAlphabet)

        # Get score of the parent-deciphered text
        parentScore = quadgramFitness(parentDeciphered, quadgramsFreq)

        count = 0
        while count < 2000:

            a = random.randint(0, len(plainAlphabet) - 1)
            b = random.randint(0, len(plainAlphabet) - 1)
            childAlphabet = parentAlphabet[:]
            # swap two characters in the child
            temp = childAlphabet.copy()
            childAlphabet[a] = temp[b]
            childAlphabet[b] = temp[a]

            # Decipher the ciperText using the child alphabet
            childDeciphered = Decrypt_RandomSubCipher(cipherText, plainAlphabet, childAlphabet)

            # Get score of the child-deciphered text
            childScore = quadgramFitness(childDeciphered, quadgramsFreq)

            if childScore > parentScore:
                # The child becomes the next parent
                parentScore = childScore
                parentAlphabet = childAlphabet[:]
                count = 0

            count += 1

        if parentScore > maxScore:
            print('\n------------ Iterarion {}'.format(realization))
            print('Score: {}'.format(parentScore))
            print('Key: {}'.format(parentAlphabet))
            print(
                'Potential plain text:\n{}'.format(Decrypt_RandomSubCipher(cipherText, plainAlphabet, parentAlphabet)))
            print('------------\n')
            maxScore = parentScore
            maxAlphabet = parentAlphabet
# -------- RANDOM SUBSTITUTION. -------- 
