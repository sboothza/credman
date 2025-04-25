import base64
import codecs
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from storage import Storage


class InvalidPasswordException(Exception):
    ...


class Passman:
    def __init__(self, storage: Storage, salt: bytes, master_password: str):
        self.passwords = {}
        self.salt = salt
        self.master_password = master_password
        self.storage: Storage = storage
        # self.load()

    def load(self):
        data = self.storage.read()
        if data != "":
            decrypted_data = self._decrypt(data)
            self.passwords = json.loads(decrypted_data)

    def save(self, new_password: str = ""):
        if new_password != "":
            self.master_password = new_password
        data = json.dumps(self.passwords)
        encrypted_data = self._encrypt(data)
        self.storage.write(encrypted_data)

    def _encrypt(self, data: str):
        salt = self.salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(str.encode(self.master_password)))
        f = Fernet(key)
        token = f.encrypt(str.encode(data))
        encrypted = codecs.decode(token)
        return encrypted

    def _decrypt(self, data: str):
        try:
            salt = self.salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=390000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(str.encode(self.master_password)))
            f = Fernet(key)
            token = f.decrypt(str.encode(data))
            decrypted = codecs.decode(token)
            return decrypted
        except:
            raise InvalidPasswordException()

    def get_password(self, key: str) -> str:
        if key in self.passwords:
            return self.passwords[key]
        return ""

    def set_password(self, key: str, password: str):
        self.passwords[key] = password

    def delete_password(self, key: str):
        if key in self.passwords:
            del self.passwords[key]
