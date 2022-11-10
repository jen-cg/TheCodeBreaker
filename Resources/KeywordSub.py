from Resources.General import *

# -------- KEYWORD SUBSTITUTION -------- 
def Incrypt_KeywordSubCipher(plainText, keyword, placement, plainAlphabet=englishAlphabet):
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

    key = {}
    for i in range(len(plainAlphabet)):
        key[plainAlphabet[i].upper()] = cipherAlphabet[i].upper()

    cipherText = ''

    for plainCharacter in plainText:

        # We will translate all letters from the plain alphabet into the cipher alphabet
        if plainCharacter.isalpha():
            cipherCharacter = key[plainCharacter]
            cipherText += cipherCharacter

        # All other characters will just be copied over
        else:
            cipherText = cipherText + plainCharacter

    return cipherText


def Decrypt_KeywordSubCipher(cipherText, keyword, placement, plainAlphabet=englishAlphabet):
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

    key = {}
    for i in range(len(plainAlphabet)):
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


def Break_KeyWordSubDictAttack(cipherText,dictionary=open('Resources/SampleTexts/englishWords3.txt').readlines(), plainAlphabet=englishAlphabet,knownLetterFrequencies=letterFrequencies_English):
    '''
    Break a keyword substitution cipher with a dictionary attack using 
    Chi-Squared statistics 
    - A "key" for this type of encryption consists of a keyword and a position
       - keywords are taken from the dictionary 
    '''
    
    # How many keys to try without an improvement before giving up
    # Here I am setting the tolerance to be ~half the number of possible keys
    tolerance = 0.5*(len(dictionary)*(26-np.mean([len([i for i in line if i.isalpha()]) for line in dictionary])))
    
    bestKeyword = []
    bestPosition = -1
    bestScore = 99e9
    
    # How many keys have been tried since the last improvement
    cnt = 0
    
    # Try words from the dictionary as the keyword 
    for keyword in dictionary:
        keyword = ''.join([i for i in keyword if i.isalpha()])
        
        # Try each possible placement of the keyword
        for position in range(0,len(plainAlphabet)-len(keyword)+1):
            decryptTest = Decrypt_KeywordSubCipher(cipherText, keyword, position, plainAlphabet=englishAlphabet)
            score = ChiSquaredStatistic(decryptTest, knownLetterFrequencies)
            
            if score < bestScore:
                cnt = 0
                bestKeyword = keyword
                bestPosition = position
                bestScore = score
                
                print(bestKeyword)
            cnt += 1
            if cnt >= tolerance:
                    return bestKeyword,bestPosition, Decrypt_KeywordSubCipher(cipherText, bestKeyword, bestPosition, plainAlphabet=englishAlphabet)
    

def Break_KeyWordSubDictAttackwCrib(cipherText,cribs,dictionary=open('Resources/SampleTexts/englishWords3.txt').readlines(), plainAlphabet=englishAlphabet,knownLetterFrequencies=letterFrequencies_English):
    '''
    Break a keyword substitution cipher with a dictionary attack using cribs
   
   - A "key" for this type of encryption consists of a keyword and a position
       - keywords are taken from the dictionary 
       
    - 'cribs' is a list of cribs to search for.  
        - Please try to be certain that the message actually contains the cribs
        - It is best to use as many cribs as you can
  
  The best solution is taken to be the key that results in the most cribs matching to the cipher text
  - If all cribs have been found the program will stop
  
  This method will work fastest/best if the keyword happens to be near the beginning of the dictionary
    '''
    
    cribs = [''.join([ c.upper() for c in i if c.isalpha()]) for i in cribs]
    
    bestKeyword = ''
    bestPosition = -1
    bestScore = 0
 
    # Try words from the dictionary as the keyword 
    for keyword in dictionary:
        keyword = ''.join([i.upper() for i in keyword if i.isalpha()])   
        # Try each possible placement of the keyword
        for position in range(0,len(plainAlphabet)-len(keyword)+1):
            
            score = 0
            for crib in cribs:
#                 print(crib)
                incryptedCrib = Incrypt_KeywordSubCipher(crib, keyword, position, plainAlphabet=englishAlphabet)
#                 print(Incrypt_KeywordSubCipher('THE', 'CAT', 0))
                
                if cipherText.find(incryptedCrib) != -1:
                    # The crib is in the cipher text
                    score += 1
            
            if score == len(cribs):
                # All of the incrypted cribs were found in the cipher text
                return keyword, position, Decrypt_KeywordSubCipher(cipherText, keyword, position, plainAlphabet=englishAlphabet)
            elif score > bestScore:
                bestKeyword = keyword
                bestPosition = position
    
    return bestKeyword, bestPosition, Decrypt_KeywordSubCipher(cipherText, bestKeyword, bestPosition, plainAlphabet=englishAlphabet)
# -------- KEYWORD SUBSTITUTION. -------- 
