import src.dictionary

def run(frequencies):
    # print("Frequencies: ", frequencies)
    #
    k = key.generateKey(frequencies)
    # print("Key: ", k.k)
    c = k.encrypt(dictionary.readCandidates('test1_candidate_5_plaintexts.txt')[1])
    #print("Ciphertext: ", c)
    # print("Plaintext: ", k.decrypt(c))


    testOne(frequencies, c)


def testOne(frequencies, c):
    """
    Takes ciphertext as input.
    Finds index of 'b' for each plaintext.
    Prints which of the 5 plaintexts matches the ciphertext.
    """
    cipher = map(int,c.split(','))
    #print cipher
    flag = 0

    plaintexts = dictionary.readCandidates('../test1_candidate_5_plaintexts.txt')
    #print plaintexts[0]
    for plaintext in plaintexts:
        bIndex = list()
        #print plaintext
        for i in range(0, len(plaintext)):
            if plaintext[i] == 'b':
                bIndex.append(i)
        #print bIndex
        testCase = cipher[bIndex[0]]

        for index in bIndex:
            if cipher[index] != testCase:
                flag = 0
                break
            else:
                flag = 1
        if flag == 1:
            print plaintext



if __name__ == '__main__':
    run({
        " ": 19,
        "a": 7,
        "b": 1,
        "c": 2,
        "d": 4,
        "e": 10,
        "f": 2,
        "g": 2,
        "h": 5,
        "i": 6,
        "j": 1,
        "k": 1,
        "l": 3,
        "m": 2,
        "n": 6,
        "o": 6,
        "p": 2,
        "q": 1,
        "r": 5,
        "s": 5,
        "t": 7,
        "u": 2,
        "v": 1,
        "w": 2,
        "x": 1,
        "y": 2,
        "z": 1
        })
