import string

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

rotor1 = {'a': 'e', 'b': 'k', 'c': 'm', 'd': 'f', 'e': 'l', 'f': 'g', 'g': 'd', 'h': 'q', 'i': 'v', 'j': 'z', 'k': 'n',
          'l': 't', 'm': 'o', 'n': 'w', 'o': 'y', 'p': 'h', 'q': 'x', 'r': 'u', 's': 's', 't': 'p', 'u': 'a', 'v': 'i',
          'w': 'b', 'x': 'r', 'y': 'c', 'z': 'j'}

rotor2 = {'a': 'a', 'b': 'j', 'c': 'd', 'd': 'k', 'e': 's', 'f': 'i', 'g': 'r', 'h': 'u', 'i': 'x', 'j': 'b', 'k': 'l',
          'l': 'h', 'm': 'w', 'n': 't', 'o': 'm', 'p': 'c', 'q': 'q', 'r': 'g', 's': 'z', 't': 'n', 'u': 'p', 'v': 'y',
          'w': 'f', 'x': 'v', 'y': 'o', 'z': 'e'}

rotor3 = {'a': 'b', 'b': 'd', 'c': 'f', 'd': 'h', 'e': 'j', 'f': 'l', 'g': 'c', 'h': 'p', 'i': 'r', 'j': 't', 'k': 'x',
          'l': 'v', 'm': 'z', 'n': 'n', 'o': 'y', 'p': 'e', 'q': 'i', 'r': 'w', 's': 'g', 't': 'a', 'u': 'k', 'v': 'm',
          'w': 'u', 'x': 's', 'y': 'q', 'z': 'o'}

reflector = ['ay', 'br', 'cu', 'dh', 'eq', 'fs', 'gl', 'ip', 'jx', 'kn', 'mo', 'tz', 'vw']

commutator = ['ac', 'df', 'rt', 'vb', 'ew', 'nm', 'ko', 'yu', 'zp', 'xj']

rState = [0, 0, 0, 0]
rState2 = False


def rotorLetterChoose(rotor, letterToSwap):
    ler = alphabet[letterToSwap]
    resletter = rotor[ler]
    # print('rot', ler, ' - ', alphabet[alphabet.index(resletter)])
    return alphabet.index(resletter)


def rotorLetterChooseReverse(rotor, letterToSwap):
    resletter = alphabet[letterToSwap]
    for seq in rotor.items():
        if seq[1] == resletter:
            # print('reverse', seq[1], ' - ', alphabet[alphabet.index(seq[0])])
            return alphabet.index(seq[0])


def reflectorMove(letterToSwap):
    resletter = alphabet[letterToSwap]
    for seq in reflector:
        if resletter in seq:
            if seq[0] == resletter:
                # print('reflector', seq[0], ' - ', alphabet[alphabet.index(seq[1])])
                return alphabet.index(seq[1])
            else:
                # print('reflector', seq[1], ' - ', alphabet[alphabet.index(seq[0])])
                return alphabet.index(seq[0])


def commutatorMove(letterToSwap):
    resletter = alphabet[letterToSwap]
    for seq in commutator:
        if resletter in seq:
            if seq[0] == resletter:
                # print('commutator', seq[0], ' - ', alphabet[alphabet.index(seq[1])])
                return alphabet.index(seq[1])
            else:
                # print('commutator', seq[1], ' - ', alphabet[alphabet.index(seq[0])])
                return alphabet.index(seq[0])
    return letterToSwap


def changeState(state):
    state[2] += 1
    state[3] += 1
    global rState2
    
    if state[2] == 22:
        state[1] += 1
        rState2 = True
    if state[1] == 5 and rState2 is True:
        rState2 = False
        state[0] += 1
        
    if state[0] == 26:
        state[0] = 0
    if state[1] == 26:
        state[1] = 0
    if state[2] == 26:
        state[2] = 0


def shiftind(letterS, shift):
    alphabett = string.ascii_lowercase
    shifted_alphabet = alphabett[shift:] + alphabett[:shift]
    table = str.maketrans(alphabett, shifted_alphabet)
    return alphabet.index(alphabet[letterS].translate(table))
    

def mainSwap(letterToSwap):
    # Изменить текущее состояние ротеров
    changeState(rState)
    
    # Найти индекс буквы
    inAlp = alphabet.index(letterToSwap)
    
    # Первый слой коммутаторов
    commutator1 = commutatorMove(inAlp)

    # Первый слой ротеров
    firstStage = rotorLetterChoose(rotor3, shiftind(commutator1, rState[2]))
    secondStage = rotorLetterChoose(rotor2, shiftind(firstStage, -rState[2] + rState[1]))
    thirdStage = rotorLetterChoose(rotor1, shiftind(secondStage, -rState[1] + rState[0]))
    
    # Рефлектор
    reflectorM = reflectorMove(shiftind(thirdStage,  -rState[0]))
    
    # Второй слой роторов
    thirdStageReverse = rotorLetterChooseReverse(rotor1, shiftind(reflectorM, rState[0]))
    secondStageReverse = rotorLetterChooseReverse(rotor2, shiftind(thirdStageReverse, -rState[0] + rState[1]))
    firstStageReverse = rotorLetterChooseReverse(rotor3, shiftind(secondStageReverse, -rState[1] + rState[2]))
    
    # Выход
    output = shiftind(firstStageReverse, -rState[2])

    # Второй слой коммутаторов
    return alphabet[commutatorMove(output)]
    

# Настройки Энигмы
print('Текущие настройки\nrotor I - A   rotor II - A    rotor III - A\nКоммутаторы:\nac, df, rt, vb, ew, nm, ko, yu, zp, xj')
settings = input('Изменить? [y/n]: ')
if settings == 'y':
    print("Настройка ротеров: (вводите начальную букву-позицию для каждого ротера")
    rState[0] = alphabet.index(input("Rotor I: ").lower())
    rState[1] = alphabet.index(input("Rotor II: ").lower())
    rState[2] = alphabet.index(input("Rotor III: ").lower())
    print("Настройка коммутаторов: (вводите пары букв для каждого коммутатора. Ни одна буква не должна повторяться)")
    for com in range(10):
        commutator[com] = input("{}-ая пара: ".format(com + 1)).lower()
        
# Основной цикл
print("Вводите по одному слову латинецей. Энигма не предусматривает пробелы.")
while True:
    letter = input("\nВведите слово: ").lower()
    if letter == "":
        break
    resStr = ''
    for ll in letter:
        resStr += mainSwap(ll)
    # print('state', rState)
    print("\nЗашифрованное слово -", resStr)
