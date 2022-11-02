import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES as AAAES

class AES():
    def __init__(self, key:str): 
        self.bs = AAAES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def Encrypt(self, raw:str) -> str:
        raw = self._pad(raw)
        iv = Random.new().read(AAAES.block_size)
        cipher = AAAES.new(self.key, AAAES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

    def Decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AAAES.block_size]
        cipher = AAAES.new(self.key, AAAES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AAAES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

if __name__ == "__main__":
    a = AES("1685pXjF(2IPucuKl23D[YZuIKd95zkmb2")

    e = a.Encrypt("enc = base64.b64decode(enc)")
    print(e)

    c = a.Decrypt(e)
    print(c)