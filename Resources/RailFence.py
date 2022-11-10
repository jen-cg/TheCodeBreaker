from Resources.General import *

# -------- RAIL FENCE TRANSLATION -------- 
def Incrypt_RailFence(plainText, key):
    
    if key == 1:
        return plainText

    # Build the fence
    fence = [ [None for i in range(len(plainText))] for rail in range(key) ]

    # Starting position on the fence
    row, column = 0,0
    going_down = True

    for i in range(len(plainText)):

        # Place the character on the fence
        fence[row][column] = plainText[i]

        # Every time we place a new letter we move over 1 column
        column += 1

        if row == key - 1:
            # then we are at the bottom of the fence and we need to move back up
            going_down = False
        if row == 0:
            # Then we are at the top of the fence and we need to move down
            going_down = True

        if going_down == False:
            row -= 1
        else: 
            row += 1

    return ''.join([c for c in np.array(fence).flatten() if c is not None])


def Decrypt_RailFence(cipherText, key):
    
    if key == 1:
        return cipherText
    
    
    # Build the fence
    fence = [ [None for i in range(len(cipherText))] for rail in range(key) ]

    # Starting position on the fence
    row, column = 0,0
    going_down = True

    for i in range(len(cipherText)):

        # Indicate spots where letters go on the fence
        fence[row][column] = i

        # Every time we place a new letter we move over 1 column
        column += 1

        if row == key - 1:
            # then we are at the bottom of the fence and we need to move back up
            going_down = False
        if row == 0:
            # Then we are at the top of the fence and we need to move down
            going_down = True

        if going_down == False:
            row -= 1
        else: 
            row += 1
            
    # Place the letters back on the fence
    index = 0
    order = []
    for i in range(key):
        for j in range(len(cipherText)):
            if str(fence[i][j]).isnumeric() and index<len(cipherText):
                order.append(fence[i][j])
                fence[i][j] = cipherText[index]
                index += 1

    dictionary = {}
    for i,c in enumerate([c for c in np.array(fence).flatten() if c is not None]):
        dictionary[order[i]] = c
        
    return ''.join([dictionary[i] for i in range(len(cipherText)) ])


def Break_RailFence(cipherText, quadgramsFreq=quadgramFreq_English):
    '''Break the Rail Fence cipher by trying all possible keys
    - Please remove all non-text characters
    - This method is fast and reliable for texts of about 500 characters or less
    
    If you have a longer text try extracting a section of ~500 characters and applying 
    this method to that section.  Once you find the key you can decipher the entire text quickly 
    '''
    
    bestKey = -99
    bestScore = -99e9
    
    for key in range(1, len(cipherText)):
        
        decryptTest = Decrypt_RailFence(cipherText, key)

        score = quadgramFitness(decryptTest, quadgramsFreq)
        if score > bestScore:
            bestKey = key
            bestScore = score
            
    return bestKey,Decrypt_RailFence(cipherText,bestKey)
# -------- RAIL FENCE TRANSLATION -------- 
