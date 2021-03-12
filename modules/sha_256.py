class binstr(object):
    '''binary string class'''
    def __init__(self, arg, bit=32):
        assert isinstance(arg, int), 'binstr must be int!'
        assert isinstance(bit, int), 'hexnum must be int!'
        self.bit = bit
        self.arg = arg % 2**(self.bit)

    def __str__(self):
        assert self.bit % 4 == 0, '__str__ is only available if bit is\
                                   divided by 4. Use __repr__ instead!'
        out = str(hex(self.arg))[2:]
        return '0' * (self.bit // 4 - len(out)) + out.upper()

    def __repr__(self):
        out = str(bin(self.arg))[2:]
        return '0' * (self.bit - len(out)) + out.upper()

    def __eq__(self, other):
        assert isinstance(other, binstr), 'other argument must be binstr!'
        if self.arg == other.arg and self.bit == other.bit:
            return True
        else:
            return False

    def __add__(self, other):
        assert isinstance(other, binstr), 'other argument must be binstr!'
        return binstr(self.arg + other.arg, max(self.bit, other.bit))

    def __radd__(self, other):
        assert isinstance(other, binstr), 'other argument must be binstr!'
        return self + other

    def __and__(self, other):
        assert isinstance(other, binstr), 'other argument must be binstr!'
        return binstr(self.arg & other.arg, max(self.bit, other.bit))

    def __invert__(self):
        return binstr((2**self.bit - 1) ^ self.arg, self.bit)

    def __xor__(self, other):
        assert isinstance(other, binstr), 'other argument must be binstr!'
        return binstr(self.arg ^ other.arg, max(self.bit, other.bit))

    def __rshift__(self, n):
        assert isinstance(n, int), 'n must be int!'
        return binstr(self.arg >> n, self.bit)

    # it is ROTARE RIGHT (I did that for "@" operand)
    def __matmul__(self, n):
        assert isinstance(n, int), 'n must be int!'
        n = n % self.bit
        out_arg = (self.arg % 2**n) * 2**(self.bit - n) + self.arg // 2**n
        return binstr(out_arg, self.bit)

    def concatenate(self, *other):
        assert isinstance(other[0], binstr), '*other arguments must be binstr!'
        if len(other) == 1:
            return binstr(self.arg * 2**other[0].bit + other[0].arg,
                          self.bit + other[0].bit)
        else:
            return (self.concatenate(other[0])).concatenate(*other[1:])

    def chunkint(self, n):
        assert isinstance(n, int), 'n must be int!'
        assert self.bit % n == 0, 'self bit must be divided by n!'
        return(binstr((self.arg // 2**i), n)
               for i in range(self.bit - n, -n, -n))

    def __lt__(self, other):
        assert isinstance(other, binstr), 'other must be binstr!'
        assert self.bit == other.bit, 'self bit must be equal other bit!'
        if self.arg < other.arg:
            return True
        else:
            return False


def text_to_binstr(text):
    assert isinstance(text, str), 'text must be string!'
    hex_text = text.encode('ascii', errors='strict').hex()
    len_hex = len(hex_text)
    return binstr(int(hex_text, 16), len_hex*4)


def sha_256(message, show=False):
    '''Пояснения:
    Все переменные беззнаковые, имеют размер 32 бита
    и при вычислениях суммируются по модулю 2^32.
    message — исходное двоичное сообщение
    m — преобразованное сообщение'''

    '''Инициализация переменных
    (первые 32 бита дробных частей квадратных корней
    первых восьми простых чисел [от 2 до 19]):'''
    h0 = binstr(0x6A09E667)
    h1 = binstr(0xBB67AE85)
    h2 = binstr(0x3C6EF372)
    h3 = binstr(0xA54FF53A)
    h4 = binstr(0x510E527F)
    h5 = binstr(0x9B05688C)
    h6 = binstr(0x1F83D9AB)
    h7 = binstr(0x5BE0CD19)

    '''Таблица констант
    (первые 32 бита дробных частей кубических корней
    первых 64 простых чисел [от 2 до 311]):'''
    k = [0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
         0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
         0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
         0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
         0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
         0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
         0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
         0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
         0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
         0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
         0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
         0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
         0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
         0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
         0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
         0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2]
    k = list(map(binstr, k))

    '''Предварительная обработка:'''
    m = message.concatenate(binstr(1, 1))
    tmp = (448 - m.bit) % 512
    m = m.concatenate(binstr(0, tmp))
    '''где tmp — наименьшее неотрицательное число, такое что
    (L + 1 + tmp) mod 512 = 448, L — число бит в сообщении
    (сравнима по модулю 512 c 448)'''
    m = m.concatenate(binstr(message.bit, 64))
    '''— длина исходного сообщения битах в виде 64-битного числа
    порядком байтов от старшего  младшему'''
    '''Далее сообщение обрабатывается последовательными порциями по 512 бит:'''
    for chunk in (m.chunkint(512)):
        w = list(word for word in chunk.chunkint(32))

        '''Сгенерировать дополнительные 48 слов:'''
        for i in range(16, 64):
            s0 = (w[i-15] @ 7) ^ (w[i-15] @ 18) ^ (w[i-15] >> 3)
            s1 = (w[i-2] @ 17) ^ (w[i-2] @ 19) ^ (w[i-2] >> 10)
            w.append(w[i-16] + s0 + w[i-7] + s1)

        '''Инициализация вспомогательных переменных:'''
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        '''Основной цикл:'''
        for i in range(64):
            sigma0 = (a @ 2) ^ (a @ 13) ^ (a @ 22)
            Ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = sigma0 + Ma
            sigma1 = (e @ 6) ^ (e @ 11) ^ (e @ 25)
            Ch = (e & f) ^ (~e & g)
            t1 = h + sigma1 + Ch + k[i] + w[i]

            h = g
            g = f
            f = e
            e = d + t1
            d = c
            c = b
            b = a
            a = t1 + t2

        '''Добавить полученные значения к ранее вычисленному результату:'''
        h0 = h0 + a
        h1 = h1 + b
        h2 = h2 + c
        h3 = h3 + d
        h4 = h4 + e
        h5 = h5 + f
        h6 = h6 + g
        h7 = h7 + h

    if show:
        print(h0, h1, h2, h3, h4, h5, h6, h7)
    '''Получить итоговое значение хеша:'''
    hash = h0.concatenate(h1, h2, h3, h4, h5, h6, h7)
    return hash


def sha_256_text(text, show=False):
    return sha_256(text_to_binstr(text), show)
