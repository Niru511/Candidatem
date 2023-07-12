from django.db import models
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from django.db import models

# key = RSA.generate(2048)
# private_key = key.export_key()
# public_key = key.publickey().export_key()

with open('private_key.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

with open('public_key.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    adharnumber = models.CharField(max_length=20)
    pannumber = models.CharField(max_length=20)
    passportnumber = models.CharField(max_length=20)

    def encrypt_number(self,phonenumber):
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_data = cipher.encrypt(phonenumber.encode())
        
        return encrypted_data

    def save(self, *args, **kwargs):
        encrypted_number1 = self.encrypt_number(self.adharnumber)
        self.adharnumber = encrypted_number1
        encrypted_number2 = self.encrypt_number(self.pannumber)
        self.pannumber = encrypted_number2
        encrypted_number3 = self.encrypt_number(self.passportnumber)
        self.passportnumber = encrypted_number3
        super(Candidate, self).save(*args, **kwargs)

    def decryptadharnum(self):
        
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(self.adharnumber)
        return decrypted_data.decode()
    

    
    def __str__(self):
         return f"{self.name}"

