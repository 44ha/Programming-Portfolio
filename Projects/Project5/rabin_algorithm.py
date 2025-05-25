import random
import math
import base64

class RabinCipher:
    @staticmethod
    def generate_keys():
        def get_prime():
            while True:
                p = random.randint(300, 400)
                if p % 4 == 3 and all(p % i != 0 for i in range(2, int(math.sqrt(p)) + 1)):
                    return p
        
        p = get_prime()
        q = get_prime()
        n = p * q
        return {
            'public_key': n,
            'private_keys': (p, q)
        }

    @staticmethod
    def encrypt(message, public_key):
        try:
            n = public_key
            message_b64 = base64.b64encode(message.encode()).decode()
            chunk_size = 1  
            chunks = [message_b64[i:i+chunk_size] for i in range(0, len(message_b64), chunk_size)]
            
            encrypted = []
            for chunk in chunks:
                m = int.from_bytes(chunk.encode(), 'big')
                if m >= n:
                    raise ValueError(f"Message chunk {m} too large for key {n}")
                c = (m * m) % n
                encrypted.append(str(c))
            
            return ','.join(encrypted)
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    @staticmethod
    def decrypt(ciphertext, p, q):
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, x, y = egcd(b % a, a)
                return g, y - (b // a) * x, x

        def modsqrt(a, p):
            if legendre_symbol(a, p) != 1:
                return 0
            elif a == 0:
                return 0
            elif p == 2:
                return 0
            elif p % 4 == 3:
                return pow(a, (p + 1) // 4, p)
            
            q = p - 1
            s = 0
            while q % 2 == 0:
                q //= 2
                s += 1
            
            z = 2
            while legendre_symbol(z, p) != -1:
                z += 1
            
            m = s
            c = pow(z, q, p)
            t = pow(a, q, p)
            r = pow(a, (q + 1) // 2, p)
            
            while t != 1:
                i = 0
                temp = t
                while temp != 1:
                    temp = (temp * temp) % p
                    i += 1
                    if i == m:
                        return 0
                
                b = pow(c, pow(2, m - i - 1), p)
                m = i
                c = (b * b) % p
                t = (t * c) % p
                r = (r * b) % p
            
            return r

        def legendre_symbol(a, p):
            ls = pow(a, (p - 1) // 2, p)
            return -1 if ls == p - 1 else ls

        try:
            n = p * q
            encrypted_chunks = [int(x) for x in ciphertext.split(',')]
            decrypted_chunks = []

            for c in encrypted_chunks:
                mp = modsqrt(c, p)
                mq = modsqrt(c, q)
                _, yp, yq = egcd(p, q)
                
                r1 = (yp * p * mq + yq * q * mp) % n
                r2 = n - r1
                r3 = (yp * p * (-mq) + yq * q * mp) % n
                r4 = n - r3

                valid_chunk = None
                for r in [r1, r2, r3, r4]:
                    try:
                        chunk_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
                        chunk = chunk_bytes.decode('ascii')
                        if all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in chunk):
                            valid_chunk = chunk
                            break
                    except:
                        continue

                if valid_chunk is None:
                    raise ValueError(f"Failed to decrypt chunk {c}")
                    
                decrypted_chunks.append(valid_chunk)

            decrypted_b64 = ''.join(decrypted_chunks)
            decrypted_message = base64.b64decode(decrypted_b64).decode()
            
            return decrypted_message
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    @staticmethod
    def get_key_type():
        return "rabin" 