from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager
import random

def upload_v(instance,filename):
    return "verification/"+str(uuid.uuid4())+"."+filename.split(".")[-1]

def upload_i(instance,filename):
    return "pfp/"+str(uuid.uuid4())+"."+filename.split(".")[-1]

def generate_otp():
    return random.randrange(100000,999999)

class Swipe(models.Model):
    first_user = models.ForeignKey("home.User", on_delete=models.CASCADE,related_name="first")
    second_user = models.ForeignKey("home.User", on_delete=models.CASCADE,related_name="second")
    type = models.CharField(max_length=63)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

class Interest(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email Address",unique=True,max_length=127)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    verification_file = models.FileField(upload_to=upload_v)
    email_is_verified = models.BooleanField(default=False)
    bio = models.CharField(max_length=1023,blank=True,null=True)
    id_is_verified = models.BooleanField(default=False)
    swipe = models.ManyToManyField(Swipe,blank=True)
    country = models.CharField(max_length=255,blank=True,null=True)
    profile_image = models.ImageField(upload_to=upload_v,blank=True,null=True)
    face_detection_probablity = models.FloatField(default=0)
    college = models.CharField(max_length=255,blank=True,null=True)
    status = models.BooleanField(default=True)
    dob = models.DateField()
    otp = models.IntegerField(default=generate_otp)
    insta_username = models.CharField(max_length=255,blank=True,null=True)
    height = models.FloatField(blank=True,null=True)
    gender = models.BooleanField()
    who_to_date = models.BooleanField()
    interests = models.ManyToManyField(Interest,blank=True)
    premium = models.BooleanField(default=False)
    is_habit_drink = models.BooleanField(blank=True,null=True)
    is_habit_smoke = models.BooleanField(blank=True,null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    # Internal
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name","phone","dob","gender","verification_file","who_to_date"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
