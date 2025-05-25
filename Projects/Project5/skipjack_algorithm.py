import random
import string

class Skipjack:
    FTABLE = [
        99, 124, 119, 123, 242, 107, 111, 197,  48,   1, 103,  43, 254, 215, 171, 118,
        202, 130, 201, 125, 250,  89,  71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
        183, 253,  147, 38,  54,  63, 247, 204,  52, 165, 229, 241, 113, 216,  49,  21,
         4, 199,  35, 195,  24, 150,   5, 154,   7,  18, 128, 226, 235,  39, 178, 117,
         9, 131,  44,  26,  27, 110,  90, 160,  82,  59, 214, 179,  41, 227,  47, 132,
        83, 209,   0, 237,  32, 252, 177,  91, 106, 203, 190,  57,  74,  76,  88, 207,
        208, 239, 170, 251,  67,  77,  51, 133,  69, 249,   2, 127,  80,  60, 159, 168,
        81, 163,  64, 143, 146, 157,  56, 245, 188, 182, 218,  33,  16, 255, 243, 210
    ]

    def __init__(self):
        self.key = None

    def _generate_key(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def _prepare_key(self, key):
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        if not key:
            raise ValueError("Key cannot be empty")
        if not all(ord(c) < 128 for c in key):
            raise ValueError("Key must contain only ASCII characters")
        return key

    def _f_function(self, input_byte, key_byte, round_num):
        index = (input_byte ^ key_byte ^ round_num) & 0x7F
        return self.FTABLE[index]

    def _process_block(self, block, key_byte, round_num, encrypt=True):
        if encrypt:
            return self._f_function(block, key_byte, round_num)
        else:
            for i in range(128):
                if self._f_function(i, key_byte, round_num) == block:
                    return i
            return block

    def encrypt(self, message, key):
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
        if not message:
            raise ValueError("Message cannot be empty")
        if not all(ord(c) < 128 for c in message):
            raise ValueError("Message must contain only ASCII characters")

        self.key = self._prepare_key(key)
        key_len = len(self.key)
        
        result = []
        for i, char in enumerate(message):
            char_val = ord(char)
            key_byte = ord(self.key[i % key_len])
            round_num = i % 256
            
            encrypted = self._process_block(char_val, key_byte, round_num, encrypt=True)
            result.append(f"{encrypted:02x}")
            
        return ''.join(result)

    def decrypt(self, ciphertext, key):
        if not isinstance(ciphertext, str):
            raise ValueError("Ciphertext must be a string")
        if not ciphertext:
            raise ValueError("Ciphertext cannot be empty")
        if not all(c in string.hexdigits for c in ciphertext):
            raise ValueError("Ciphertext must be a hex string")
        if len(ciphertext) % 2 != 0:
            raise ValueError("Invalid ciphertext length")

        self.key = self._prepare_key(key)
        key_len = len(self.key)
        
        result = []
        for i in range(0, len(ciphertext), 2):
            encrypted = int(ciphertext[i:i+2], 16)
            key_byte = ord(self.key[(i//2) % key_len])
            round_num = (i//2) % 256
            
            decrypted = self._process_block(encrypted, key_byte, round_num, encrypt=False)
            result.append(chr(decrypted))
            
        return ''.join(result)

    @staticmethod
    def get_key_type():
        return "skipjack" 