from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import base64

def encrypt_string_rsa(message):
    byte_message = str.encode(message)
    with open('public_key.pem', 'rb') as f:
        public_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(public_key)
    encrypted_string = cipher.encrypt(byte_message)
    encrypted_string = base64.b64encode(encrypted_string).decode('utf-8')
    return encrypted_string


def decrypt_string_rsa(encrypted_message):
    decoded_hash_string = base64.b64decode(encrypted_message)
    with open('private_key.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(private_key)
    result_string = cipher.decrypt(decoded_hash_string).decode()

    return result_string


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    adharnumber = models.TextField(blank=True, null=True)
    pannumber = models.TextField(blank=True, null=True)
    passportnumber = models.TextField(blank=True, null=True)

    def decrypt_adharnumber(self):
        if self.adharnumber:
            decrypted_data = decrypt_string_rsa(self.adharnumber)
            return decrypted_data

    def decrypt_pannumber(self):
        if self.pannumber:
            decrypted_data = decrypt_string_rsa(self.pannumber)
            return decrypted_data

    def decrypt_passportnumber(self):
        if self.passportnumber:
            decrypted_data = decrypt_string_rsa(self.passportnumber)
            return decrypted_data

    def __str__(self):
        return f"{self.name}"


@receiver(pre_save, sender=Candidate)
def encrypt_and_save(instance, *args, **kwargs):
    adharnumber = instance.adharnumber
    pannumber = instance.pannumber
    passportnumber = instance.passportnumber
    if adharnumber:
        encrypted_data = encrypt_string_rsa(adharnumber)
        instance.adharnumber = encrypted_data

    if pannumber:
        encrypted_data = encrypt_string_rsa(pannumber)
        instance.pannumber = encrypted_data

    if passportnumber:
        encrypted_data = encrypt_string_rsa(passportnumber)
        instance.passportnumber = encrypted_data
