import math
import random


def multiplicative_inverse(a, b):
    vector = []
    c1 = max(a, b)
    a = min(a, b)
    b = c1
    while a % b != 0:
        c = a % b
        a = b
        b = c
        vector.append((a, b))
    result = [[0, 1] for i, x in enumerate(vector)]
    for i in range(len(vector) - 2, -1, -1):
        result[i][0] = result[i + 1][1]
        result[i][1] = result[i + 1][0]
        result[i][1] -= result[i + 1][1] * (vector[i][0] // vector[i][1])
    return result[0][1] % c1


def gcd(a, b): # Реализация алгоритма Евклида
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def is_prime(n): # Функция проверяет, является ли число простым 
    if n == 1:
        return False
    numb = (math.sqrt(n)) # считаем квадратный корень из n
    for i in range(2, int(numb + 3)):
        if i == n:
            break
        if n % i == 0: 
            return False
    return True


def generate_keypair(p, q): # Генерация ключей
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Оба числа должны быть простыми.')
    elif p == q:
        raise ValueError('p и q не равны')
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


if __name__ == '__main__':
    print("RSA зашифрован/ Расшифрован")
    p = int(input("Введите простое число для генерации ключей : "))
    q = int(input("Введите другое простое число: "))
    public, private = generate_keypair(p, q)
    print("Ваш публичный ключ ", public, " и ваш приватный ключ ", private)
    statement = input("Введите слово\число : ")
    encrypted_st = encrypt(private, statement)
    print("Ваш зашифрованный текст: ")
    print(''.join(map(lambda x: str(x), encrypted_st)))
    print("Ваше слово:")
    print(decrypt(public, encrypted_st))
    input()
    