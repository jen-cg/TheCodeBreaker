from Resources.General import *

# -------- HILL CIPHER -------- 
def Incrypt_2x2Hill( plainText, key, plainAlphabet=englishAlphabet ):
    '''
    **Incrypt a 2x2 Hill Cipher**
    
    key is a list of key-matrix elements in the order:
    key = [k_1, k_2, k_3, k_4] = [ k_1  k_2 ]
                                 [ k_3  k_4 ]
        
    You can customize the encryption further by reordering the alphabet
        - ex) Reverse the alphabet: englishAlphabet[::-1]
    '''
    k1, k2, k3, k4 = np.array(key).flatten()
    
    if len(plainText)%2 != 0:
        print('Invalid plain text length.  The length of the plain text must be a multiple of 2.')
        return    
    if k1*k4 - k2*k3 == 0 or gcd(k1*k4 - k2*k3, len(plainAlphabet)) != 1:
        print('Invalid key.  The determinant of the key must be non-zero and coprime to the length of the alphabet.')
        return 

    
    letter2num = { c.upper():i for i , c in enumerate(plainAlphabet) }
    num2letter = { i:c.upper() for i , c in enumerate(plainAlphabet) }
    
    cipherText = ''
    # Read the message in groups of vectors of length 2
    for i in range(0,len(plainText), 2):
        
        p1, p2 = [ letter2num[letter] for letter in list(plainText[i:i+2]) ]
        
        c1 = num2letter[(k1*p1 + k2*p2)%len(plainAlphabet)]
        c2 = num2letter[(k3*p1 + k4*p2)%len(plainAlphabet)]
        
        cipherText += c1 + c2
    
    return cipherText


def Decrypt_2x2Hill( cipherText, key, plainAlphabet=englishAlphabet):
    '''
    **Decrypt a 2x2 Hill Cipher**
    
    key is a list of key-matrix elements in the order:
    key = [k_1, k_2, k_3, k_4] = [ k_1  k_2 ]
                                 [ k_3  k_4 ]
        
    You can customize the encryption further by reordering the alphabet
        - ex) Reverse the alphabet: englishAlphabet[::-1]
    ''' 
    k1, k2, k3, k4 = np.array(key).flatten()
    
    if len(cipherText)%2 != 0:
        print('Invalid cipher text length.  The length of the cipher text must be a multiple of 2.')
        return 
    if k1*k4 - k2*k3 == 0 or gcd(k1*k4 - k2*k3, len(plainAlphabet)) != 1:
        print('Invalid key.  The determinant of the key must be non-zero and coprime to the length of the alphabet.')
        return 
    
    letter2num = { c.upper():i for i , c in enumerate(plainAlphabet) }
    num2letter = { i:c.upper() for i , c in enumerate(plainAlphabet) }

    dInvrt = pow(int((k1*k4 - k2*k3) % len(plainAlphabet)), -1,len(plainAlphabet))
    
    KInvrt_1 =  dInvrt*k4 % len(plainAlphabet)
    KInvrt_2 = -dInvrt*k2 % len(plainAlphabet)
    KInvrt_3 = -dInvrt*k3 % len(plainAlphabet)
    KInvrt_4 =  dInvrt*k1 % len(plainAlphabet)
    
    
    plainText = ''
    # Read the message in groups of vectors of length 2
    for i in range(0,len(cipherText), 2):
        c1, c2 = [ letter2num[letter] for letter in list(cipherText[i:i+2]) ]
        
        p1 = num2letter[(KInvrt_1*c1 + KInvrt_2*c2)%len(plainAlphabet)]
        p2 = num2letter[(KInvrt_3*c1 + KInvrt_4*c2)%len(plainAlphabet)]
    
        plainText += p1 + p2
    
    return plainText


def Break_2x2HillBruteForce( cipherText,plainAlphabet=englishAlphabet, knownLetterFrequencies=letterFrequencies_English ):
    '''
    **Break a 2x2 Hill Cipher with a Brute Force Attack **
    
    The 2x2 Hill cipher has few enough possible keys that a brute force attack 
    is possible (though not always fast).  Here every possible key is checked and 
    the resulting decryption is assessed using Chi-Squared Statistics.
    
    -Please remove all non-text characters before using
    '''
    
    if len(cipherText)%2 != 0:
        print('Invalid cipher text length.  The length of the cipher text must be a multiple of 2.')
        return 

    bestKey = []
    bestScore = 99e99
    
    possibleKeys = []
    for key in itertools.permutations(list(range(0,len(plainAlphabet))), 4):
        k1, k2, k3, k4 = np.array(key).flatten()
        if k1*k4 - k2*k3 != 0 and gcd(k1*k4 - k2*k3, len(plainAlphabet)) == 1:
            possibleKeys.append(key)
    
    for key in possibleKeys:
        decryptTest = Decrypt_2x2Hill( cipherText, key, plainAlphabet)
        score = ChiSquaredStatistic(decryptTest, knownLetterFrequencies)
        if score < bestScore:
            bestScore = score
            bestKey = key
    
    return bestKey, Decrypt_2x2Hill( cipherText, bestKey, plainAlphabet)


def Break_2x2HillBigramMatching( cipherText,b1,m1,b2,m2, plainAlphabet=englishAlphabet):
    '''
    **Break a 2x2 Hill Cipher with Bigram Matching**
    
    bigram1 = b1 = a bigram in the cipher text
    match1  = m1 = the likley plain text version of b1
        - If you choose b1 to be the most common bigram in the
        cipher text, then m1 = 'TH'  would be logical
    
    bigram2 = b2 = another bigram in the cipher text
    match2  =  m2 = the likley plain text version of b2
            - If you choose b2 to be the second most common bigram in the
        cipher text, then m2 = 'HE'  would be logical
    
    -Please remove all non-text characters before using
    '''
    
    if len(cipherText)%2 != 0:
        print('Invalid cipher text length.  The length of the cipher text must be a multiple of 2.')
        return 
    
    letter2num = { c.upper():i for i , c in enumerate(plainAlphabet) }
    num2letter = { i:c.upper() for i , c in enumerate(plainAlphabet) }
    
    
    m11, m12 = [ letter2num[c] for c in list(m1)]
    m21, m22 = [ letter2num[c] for c in list(m2)]
    
    b11, b12 = [ letter2num[c] for c in list(b1)]
    b21, b22 = [ letter2num[c] for c in list(b2)]
    
    dInvert = pow(int((m11*m22 - m21*m12) % len(plainAlphabet)), -1,len(plainAlphabet))  
#     print(dInvert)
    
#     print('P = ')
#     print(m11, m21)
#     print(m12, m22)
    
#     print('\n')
    
#     print('C = ')
#     print(b11, b21)
#     print(b12, b22)
       
#     print('\n')
    
#     print('P^-1 = ')
#     print(dInvert*m22 % len(plainAlphabet), -dInvert*m21 % len(plainAlphabet))
#     print(-dInvert*m12 % len(plainAlphabet), dInvert*m11 % len(plainAlphabet))
    
    k1 = dInvert*( b11*m22 - b21*m12 ) % len(plainAlphabet) 
    k2 = dInvert*(-b11*m21 + b21*m11 ) % len(plainAlphabet)
    k3 = dInvert*( b12*m22 - b22*m12 ) % len(plainAlphabet)
    k4 = dInvert*(-b12*m21 + b22*m11 ) % len(plainAlphabet)
    
    key = [k1,k2,k3,k4]

    if k1*k4 - k2*k3 != 0 and gcd(k1*k4 - k2*k3, len(plainAlphabet)) == 1:
        return key, Decrypt_2x2Hill( cipherText, key, plainAlphabet)
    else:
        return None

    
def Break_2x2HillCrib( cipherText,crib, plainAlphabet=englishAlphabet, knownLetterFrequencies=letterFrequencies_English):
    '''
    ** Break a 2x2 Hill Cipher with a Crib **
    
    The crib message is "dragged" across the cipher text
        - We place the crib at different positions along the cipher text
        and extract potential bigram matches 
    
        - The crib must be 5 letters long
        
        - Try the most common 5grams: 'OFTHE' 'INTHE' 'ATION' 'THERE' 'TOTHE' 'ANDTH'
    '''
    if len(cipherText)%2 != 0:
        print('Invalid cipher text length.  The length of the cipher text must be a multiple of 2.')
        return 
    
    bestScore = 99e99
    bestKey = [ ]
    
    for i in range(0, len(cipherText)-len(crib)):
        if i % 2 == 0:
            m1 = crib[:2]
            b1 = cipherText[i:i+2]
            m2 = crib[2:4]
            b2 = cipherText[i+2:i+4]
        else:
            m1 = crib[1:3]
            b1 = cipherText[i+1:i+3]
            m2 = crib[3:5]
            b2 = cipherText[i+3:i+5]
            
        BreakTest = Break_2x2HillBigramMatching( cipherText,b1,m1,b2,m2, plainAlphabet)
        if BreakTest != None:
            key, decryptTest  = BreakTest
            score = ChiSquaredStatistic(decryptTest)
            if score < bestScore:
                bestScore = score
                bestKey = key
    return bestKey, Decrypt_2x2Hill( cipherText, bestKey, plainAlphabet)
     
# -------- HILL CIPHER. -------- 
