from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from .mymanager import UserManager


class Branch(models.Model):
    Branch_id = models.AutoField(primary_key=True)
    Branch_name = models.CharField(max_length=255)
    zone = models.ForeignKey(
        "Zone", on_delete=models.CASCADE, related_name="branches")

    def __str__(self):
        return self.Branch_name


class Zone(models.Model):
    Zone_id = models.AutoField(primary_key=True)
    Zone_name = models.CharField(max_length=255)
    head_office = models.ForeignKey(
        "HeadOffice", on_delete=models.CASCADE, related_name="related_zones")

    def __str__(self):
        return self.Zone_name


class HeadOffice(models.Model):
    HeadOffice_id = models.AutoField(primary_key=True)
    HeadOffice_name = models.CharField(max_length=255, default="Mizynté")

    def __str__(self):
        return self.HeadOffice_name


class CustomUser(AbstractUser):
    User_id = models.AutoField(primary_key=True)
    Phone_number = models.CharField(max_length=15, unique=True)
    Phone_is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)

    ACCESS_LEVEL_CHOICES = [
        ("employee", "Employee"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    ]
    access_level = models.CharField(
        max_length=10, choices=ACCESS_LEVEL_CHOICES)
    branch = models.CharField(max_length=22)
    zone = models.CharField(max_length=22)
    head_office = models.CharField(max_length=22)

    USERNAME_FIELD = "Phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()
