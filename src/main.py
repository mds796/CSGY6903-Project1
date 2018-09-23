import key

def run(frequencies):
    print("Frequencies: ", frequencies)

    k = key.generateKey(frequencies)
    print("Key: ", k)

    print("Ciphertext: ", key.encrypt("Hello, World!", k))


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
