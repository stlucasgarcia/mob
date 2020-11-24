"""
Security module responsable to all kind of encrypt and decrypt.
"""


import base64
from os import path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Cryptography:
    @staticmethod
    def generate_key_derivation(salt: bytes, master_password: str) -> None:
        """Generate 256 bits key and storaged in 'encryption.key' in binary."""

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

        with open(
            path.abspath("moodleapi").split("moodleapi")[0] + "encryption.key",
            "wb",
        ) as key_file:
            key_file.write(key)

    @staticmethod
    def load_key() -> bytes:
        """Load de previous key created and storaged in 'encryption.key'
        in binary."""

        return open(
            path.abspath("moodleapi").split("moodleapi")[0] + "encryption.key",
            "rb",
        ).read()

    @staticmethod
    def encrypt(value_to_encrypt: str) -> str:
        """With the key loaded, you can encrypt any string in this
        function and will return the message encrypted."""

        f = Fernet(Cryptography.load_key())
        encrypted_key = f.encrypt(value_to_encrypt.encode())

        return str(encrypted_key)

    @staticmethod
    def decrypt(encrypted_key: bytes) -> str:
        """Decrypt an message previously encrypted and will be returned
        the real string."""

        f = Fernet(Cryptography.load_key())
        try:
            return f.decrypt(encrypted_key).decode()

        except InvalidToken:
            raise InvalidToken("Invalid Token")
