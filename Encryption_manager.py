class EncryptionManager:
    def __init__(self, shift=7):
        self.shift = shift

    def encrypt_embedding(self, embedding):
        return embedding + self.shift

    def decrypt_embedding(self, encrypted):
        return encrypted - self.shift