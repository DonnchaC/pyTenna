"""
GoTenna encryption algorithim
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
    Implement encryption and decryption of Gotenna files
    """
    def __init__(self, key_bytes, package_name="com.gotenna.gotenna"):
        self.key = hashlib.pbkdf2_hmac('sha1', package_name, key_bytes, 1000, 16)
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
            try:
                return pkcs5_unpad(cipher.decrypt(base64.b64decode(enc)))
            except Exception:
                return None
        return pkcs5_unpad(cipher.decrypt(enc))


def test_sample_keys():
    APP_NAME = "com.gotenna.sdk.sample"
    KEY = "+N9h2A0tMtRsORktjn5QGg=="

    PLAINTEXT = "A" * 32
    ENCRYPTED = "mI1yF5m/hfTxwjHD+ToJXXeE/pmaBKaQsacsGXgXNZZx+9W4dSfS8lvCsKtMOlVi"

    cipher = GoTennaAESCipher(base64.b64decode(KEY), package_name=APP_NAME)
    encrypted = cipher.encrypt(PLAINTEXT, base64_encode=True)
    assert encrypted == ENCRYPTED

    decrypted = cipher.decrypt(encrypted, base64_encode=True)
    assert decrypted == PLAINTEXT


def test_real_keys():
    KEY = "ug2LMO93jeLX0+N1tzM9sA=="
    ENCRYPTED = """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
MMLvLAorlloR/SlDkAQunnNJ/fMn3obqeg=="""
    encrypted = base64.b64decode("".join(ENCRYPTED.splitlines()))
    cipher = GoTennaAESCipher(base64.b64decode(KEY))
    assert "Finished Loading Group Secrets" in cipher.decrypt(encrypted)


if __name__ == "__main__":
    test_sample_keys()
    test_real_keys()

    import argparse

    parser = argparse.ArgumentParser(description='Decrypted Gotenna file')

    parser.add_argument('key', metavar='KEY', type=str, help='Base64 encoded key')
    parser.add_argument('file', metavar='FILE', type=str, help='File to decrypt')
    parser.add_argument('--package-name', type=str, default='com.gotenna.gotenna')

    args = parser.parse_args()

    with open(args.file, "r") as encrypted_file:
        encrypted_data = base64.b64decode("".join(encrypted_file.read().splitlines()))

    cipher = GoTennaAESCipher(base64.b64decode(args.key), args.package_name)
    print(cipher.decrypt(encrypted_data))


