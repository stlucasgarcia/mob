"""
Security module responsable to all kind of encrypt and decrypt.
"""

from cryptography.fernet import Fernet

from os import path


class Cryptography:
    """Cryptography class is responsable to generate an public and private key,
    encrypt and decrypt messages by staticmethods"""

    @staticmethod
    def generate_key():
        """Create an file with both public and private key for encrypt
        and decrypt respectively."""

        key = Fernet.generate_key()

        with open(path.abspath('bot').split('bot')[0] + "encryption.key", 'wb') as key_file:
            key_file.write(key)


    @staticmethod
    def load_key():
        """Load de previous key created and storaged in 'encryption.key'
        in binary."""

        return open(path.abspath('bot').split('bot')[0] + "encryption.key", 'rb').read()


    @staticmethod
    def encrypt_message(message=None, *args, **kwargs):
        """With the key loaded, you can encrypt any string in this
        function and will return the message encrpyted."""

        if message:
            key = Cryptography.load_key()
            encoded_message = message.encode()

            f = Fernet(key)
            encrypted_message = f.encrypt(encoded_message)

            return encrypted_message.decode('utf-8')

        else:
            raise ValueError('Message not provided.')


    @staticmethod
    def decrypt_message(encrypted_message=None):
        """Decrypt an message previusly encrypted and will be returned
        the real string."""

        if encrypted_message:
            key = Cryptography.load_key()
            f = Fernet(key)

            decrypted_message = f.decrypt(encrypted_message).decode()

            return decrypted_message

        else:
            raise ValueError('Encrypted message not provided.')
