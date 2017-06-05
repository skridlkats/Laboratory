def GetMode():
    print("Выберите 'e' (для шифрования) или 'd' (для расшифрования)")
    mode = input()
    if mode in "e d".split():
        return mode
    else:
        print("Выберите 'x' или 'y' ")
        GetMode()


def Vigenere_Encryption(mode, statement, key):
    if mode == "e":
        result = ""
        key1 = ""
        while len(key1) < len(statement):
            key1 = key1 + key
        for i in range(len(statement)):
            UpperReg = 0
            j = ord(key1[i])
            t = ord(statement[i])
            if t <= ord("Z"):
                UpperReg = 1
            if j <= ord("Z"):
                j -= ord("A")
            elif j >= ord("a"):
                j -= ord("a")
            if UpperReg == 0:
                if (t + j) > ord("z"):
                    t -= 26
            if UpperReg == 1:
                if (t + j) > ord("Z"):
                    t -= 26
            result += chr(t + j)
        return result
    else:
        result = ""
        key1 = ""
        while len(key1) < len(statement):
            key1 = key1 + key
        for i in range(len(statement)):
            UpperReg = 0
            j = ord(key1[i])
            t = ord(statement[i])

            if t <= ord("Z"):
                UpperReg = 1

            if j <= ord("Z"):
                j -= 65
            elif j >= ord("a"):
                j -= 97

            if UpperReg == 0:
                if (t - j) < ord("a"):
                    t += 26
            if UpperReg == 1:
                if (t - j) < ord("A"):
                    t += 26

            result += chr(t - j)
        return result


mode = GetMode()

statement = input("Введите текст: ")
key = input("Введите ключ: ")

print("Зашифрованный текст :  " + Vigenere_Encryption(mode, statement, key))
