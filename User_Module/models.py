from django.db import models
from django.contrib.auth.hashers import make_password


class Farmer(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def set_password(self, raw_password):
        """Hashes the password and sets it."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Compares a raw password to the stored hashed password."""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)