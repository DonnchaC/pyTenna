#!/usr/bin/env python2
"""
goTenna encryption algorithm for Android shared preferences, application
and log data.

The Android app stores its unique encryption key in the shared preferences
directory.
"""
import hashlib
import base64

from Crypto.Cipher import AES


def pkcs5_pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)


def pkcs5_unpad(s):
    return s[0:-ord(s[-1])]


class GoTennaAESCipher:
    """
    Implement encryption and decryption of goTenna files

    The package name is name of the Android application package. This needs
    to be change if using the SDK as part of another application.
    """
    def __init__(self, key_bytes, package_name="com.gotenna.gotenna"):
        self.key = hashlib.pbkdf2_hmac('sha1', package_name.encode("utf-8"), key_bytes, 1000, 16)
        self.iv = "\x00" * 16
        self.mode = AES.MODE_CBC

    def encrypt(self, raw, base64_encode=False):
        cipher = AES.new(self.key, self.mode, self.iv)
        encode = cipher.encrypt(pkcs5_pad(raw))
        if base64_encode:
            return base64.b64encode(encode)
        return encode

    def decrypt(self, enc, base64_encode=False):
        cipher = AES.new(self.key, self.mode, self.iv)
        if base64_encode:
            return pkcs5_unpad(cipher.decrypt(base64.b64decode(enc)))
        return pkcs5_unpad(cipher.decrypt(enc))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Decrypted goTenna file')

    parser.add_argument('key', metavar='KEY', type=str, help='Base64 encoded key')
    parser.add_argument('file', metavar='FILE', type=str, help='File to decrypt')
    parser.add_argument('--package-name', type=str, default='com.gotenna.gotenna')

    args = parser.parse_args()

    with open(args.file, "r") as encrypted_file:
        encrypted_data = base64.b64decode("".join(encrypted_file.read().splitlines()))

    cipher = GoTennaAESCipher(base64.b64decode(args.key), args.package_name)
    print(cipher.decrypt(encrypted_data))


