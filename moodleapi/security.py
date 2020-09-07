"""
Security module responsable to all kind of encrypt and decrypt.
"""

from cryptography.fernet import Fernet


class Cryptography:

    def __init__(self):
        pass


    def generate_key(self):
        """Create an file with both public and private key for encrypt
        and decrypt respectively."""

        key = Fernet.generate_key()

        with open('encryption.key', 'wb') as key_file:
            key_file.write(key)


    def load_key(self):
        """Load de previous key created and storaged in 'encryption.key'
        in binary."""

        return open('encryption.key', 'rb').read()


    def encrypt_message(self, message=None, *args, **kwargs):
        """With the key loaded, you can encrypt any string in this
        function and will return the message encrpyted."""

        if message:
            key = Cryptography.load_key(self)
            encoded_message = message.encode()

            f = Fernet(key)
            encrypted_message = f.encrypt(encoded_message)

            return [[encrypted_message],]

        else:
            raise ValueError('Message not provided.')


    def decrypt_message(self, encrypted_message=None):
        """Decrypt an message previusly encrypted and will be returned
        the real string."""

        if encrypted_message:
            key = Cryptography.load_key(self)
            f = Fernet(key)

            decrypted_message = f.decrypt(encrypted_message).decode()

            return [[decrypted_message],]

        else:
            raise ValueError('Encrypted message not provided.')
