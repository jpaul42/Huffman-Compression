# -*- coding: utf-8 -*-
#
# compress.py
#
# hw9pr2 ~ cs5black
#

# This is a placeholder file for the Huffman compression problem
# It also illustrates the "main" trick...

# The code below should run when loading the file:

#
# compress.py
#
# hw9pr2 ~ cs5black
#

# This is a placeholder file for the Huffman compression problem
# It also illustrates the "main" trick...

# The code below should run when loading the file:

"""
Ended up not using findScore(), getElement(), and typeCheck because findScore and getElement were simple enough
functions that could be easily written in a larger function. typeCheck was not used because I restructured my huffman tree
such that the composing lists all had integers in their zeroth indeces."""


prefixCodes = {} # dictionary containing the prefix codes

def main():
    """This function runs automatically due to the “main trick”. It calls helper functions that cause a file
    to be read, find the frequencies of each of the characters, organize/order the frequencies, build a huffman
    tree, find the prefixes of each character in the huffman tree, and then compress the file."""
    openedFile, fileName = getFile() # opening file specified by user
    textString = openedFile.read() # Capturing all the characters in the text file and storing the string in 'textString'
    dictionary, inputBytes = getFrequencies(textString) # Creating dictionary of frequencies
    frequencyList = takeFrequencies(dictionary) # Converting the frequencies in the dictionary into a list
    orderedList = orderFrequencies(frequencyList) # Sorting the frequency list
    dictionaryList = dicToList(dictionary) # Converting the original dictionary into a list
    orderedDic = orderedDicList(orderedList, dictionaryList) # Sorting the dictionary list using the sorted frequency list
    huffTree = Huffman(orderedDic) # Building the huffman tree
    Prefix(huffTree[0],"") # putting the prefix codes into the dictionary 'prefixCodes'
    binaryString = charToPrefix(textString, prefixCodes) # Converting the original text in the file into a sequence of bits using prefix codes
    binaryCompress, byteNum = binaryToChar(binaryString) # Converting the string of binary into a smaller string of representative characters
    dictionaryBytes = writeFile(binaryCompress, prefixCodes, fileName) # Writing this string of characters to a new file
    # Printing stats. Get the same stats for all fields except for ones related to the dictionary because of different representation!!!
    print "Original file: " + fileName
    print "Total bytes: " + str(inputBytes)
    print "Number of different characters in the file: " + str(len(dictionary))
    print
    print "Compressed file: " + fileName + ".HUFFMAN"
    print "Dictionary overhead in bytes: " + str(dictionaryBytes)
    print "Compressed text length in bytes: " + str(byteNum)
    print "Total length in bytes: " + str(dictionaryBytes + byteNum)
    print "Actual compression ratio: " + str((float)(dictionaryBytes + byteNum)/(float)(inputBytes))
    print "Asymptotic compression ratio: " + str((float)(byteNum)/(float)(inputBytes))
    

def getFile():
    """This function opens the file so that it can be read by the program. 
    This function returns the name of the file as well as the file itself"""
    fileName = raw_input("Enter the name of a file: ") #user input file name to be opened
    handle = open(fileName, "rb")
    return handle, fileName

def getFrequencies(S):
    """This function takes a string ’S’ which contains all of the letters in a text file. 
    The function then parses the string and places each of the character’s frequencies in a dictionary
    called ‘frequencies’. This function returns ‘frequencies’ and ‘numBytes’, the number of Bytes 
    in the original text file."""
    frequencies = {} # setting up dictionary of frequencies
    for i in range(len(S)):
        if frequencies.has_key(S[i]):
            frequencies[S[i]] = frequencies[S[i]] + 1 # updating frequencies when recurrent letter is encountered
        else:
            frequencies[S[i]] = 1 # adding new entry to dictionary
    numBytes = len(S)
    return frequencies, numBytes

def takeFrequencies(D):
    """This function takes the dictionary returned by getFrequencies and places the
    frequencies (the entries) corresponding to each key into a list. This new list, called freqList is returned"""
    freqList = []
    for key in D:
        freqList += [D[key]] # converting frequencies in dictionary into list
    return freqList

def orderFrequencies(L):
    """This function orders the frequencies that were obtained in the function ‘takeFrequencies’.
    The frequencies are ordered from smallest to largest because this is key to the algorithm 
    that creates the Huffman tree. This function returns this ordered list"""
    if len(L) == 0:
        return []
    else:
        minNum = reduce(lambda x, y: min(x,y), L) # finding smallest frequency in list and adding it to list that will be returned. List ordered from smallest to largest frequency
        for a in range(len(L)):
            if(minNum == L[a]):
                return [reduce(lambda x, y: min(x,y), L)] + orderFrequencies(L[:a] + L[a+1:])

def dicToList(D):
    """This function takes the dictionary ‘D’ returned by getFrequencies and places each of the
    key : element pairs as lists in a larger list. This function returns this list of lists."""
    dicList = []
    for key in D:
        dicList += [[D[key], key]] # converting key : element pairs in dictionary into [key,element] pairs
    return dicList

def orderedDicList(L1,L2):
    """This function orders the entries in the dictionary that was converted into a list 'L2'
    (returned by dicToList) by frequency, using the list returned by ‘orderFrequencies’ 'L1' as a guide.
    The ordered dictionaryList is returned"""
    if (len(L1) == 0) or (len(L2) == 0):
        return []
    else: 
        for b in range(len(L2)):
            if(L2[b][0] == L1[0]): # using L1 as guide to sort L2
                return [[L2[b][0],L2[b]]] + orderedDicList(L1[1:],L2[:b] + L2[b+1:])

def createPair(L):
    """This function takes the first two entries from the ordered dictionaryList ‘L’
    and pairs them together into a list that contains the sum of the two elements’ 
    frequencies as well as two lists containing each of the letters and their frequencies. 
    This will be called repeatedly to form the Huffman Tree. This function returns the list 
    containing the pair of elements."""
    element1List = L[0]
    element2List = L[1]
    pairSum = element1List[0] + element2List[0] # finding sum of frequencies of pair
    jointList = [pairSum] + [element1List] + [element2List] # creating new list containing pair
    return jointList

# L1 is the clump we're tyring to insert into the huffman list (L2)
def insert(L1, L2):
    """Similar to the insert function we wrote earlier for the insertion sort, this function
    will insert a list ‘L1’ containing certain letters into a larger list ‘L2’ containing
    individual letters or lists of letters based on frequency scores indicated in the first index of the list ‘L1’."""
    if L2 == []:
        return [L1]
    elif L1[0] < L2[0][0]: # Insertion based on frequency value
        return [L1] + L2
    else: 
        return [L2[0]] + insert(L1, L2[1:])

def Huffman(L):
    """This function builds a Huffman tree for list ‘L’ by recursively
    calling the insert and createPair helper functions."""
    if len(L) == 0:
        return []
    elif len(L) == 1:
        return L
    else:
        return Huffman(insert(createPair(L), L[2:])) # recursively building huffman tree by building one 'pair' at a time, recursively

# Traverse the huffman tree in the same way that we built the fractal tree!!! L = subtree. S is the prefix up to that point
def Prefix(L,S):
    """This function, takes list ‘L’, which is a Huffman tree and recursively builds all
    the prefix codes. As they are being built, the prefix codes are stored in ’S’. 
    Once the prefixes are built, they are stored in a dictionary. The dictionary is returned."""
    if len(L) <= 1:
        return
    elif len(L) == 3:
        Prefix(L[1],S + "0") # index 1 is always the left subtree. Adding 0 to prefix if we go down left subtree.
        Prefix(L[2],S + "1") # index 2 is always the right subtree. Adding 1 to prefix if we go down right subtree
    else:
        prefixCodes[L[1][1]] = S # adding the prefix code to the dictionary of prefix codes
        return

# Converting Prefix Codes into ints so that we can use the ints to form characters out of 8 bits of binary
def baseBToNum(S, B):
    """This function was built in a prior homework. It takes a string ’S’ which represents a number
    in base ‘B’ and converts it to a number in base 10. This base 10 number is returned"""
    if len(S) == 0:
        return 0
    else:
        return baseBToNum(S[1:],B) + int(S[0])*(B**(len(S) - 1))
        
def charToPrefix(S, D):
    """This function takes all of the characters in the original text file ’S’ 
    and converts them to binary using the prefix codes stored in dictionary ‘D’."""
    binaryString = ""
    for i in range(len(S)):
        binaryString += D[S[i]] #iteratively transforming chars in original text file into sequence of bits
    return binaryString
    
def binaryToChar(S):
    """This function takes 8 bit sequences of 0s and 1s and converts them into characters using their value in binary."""
    charString = ""
    byteCount = 0
    while len(S) >= 8:
        num = baseBToNum(S[:8],2) # finding value of 8 bit sequence in base 10
        charString += chr(num) # converting the number in base 10 into character using ASCII value
        S = S[8:]
        byteCount += 1
    charString += chr(baseBToNum(S,2))
    byteCount += 1
    return charString, byteCount
    
def writeFile(S,D, name):
    """This function creates a new file that has the name stored in ‘name’ and a “.HUFFMAN” ending.
    At the top of the file, the function transcribes the dictionary ‘D’. After that, 
    the function transcribes string ’S’ which is the compressed text."""
    huffman = open(name + ".HUFFMAN", "wb")
    dictionaryBytes = 0
    for key in D:
        huffman.write("'" + str(key) + "'" + " - " + D[key]) # Creating glossary of elements in the dictionary at the beginning of new text file
        huffman.write('\n')
        dictionaryBytes += 6 + len(key) + len(D[key]) 
    huffman.write('\n')
    dictionaryBytes += 1
    huffman.write(S) # Transcribing the compressed text onto the file after the dictionary glossary
    huffman.close()
    return dictionaryBytes

if __name__ == "__main__":
   main()



