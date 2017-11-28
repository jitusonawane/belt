from __future__ import unicode_literals
from django.db import models 
import re
import bcrypt
import datetime 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z]{2,}$')
PASS_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', re.MULTILINE)

class UserManager(models.Manager):
    
    def reg_validator(self, postData):
        
        errors = {}
              
        #first name and last name check!

        if len(postData['name']) <2:            
            errors['1'] = "First Name Is too Short!"
            print "this is error one "
                           
        if len(postData['username']) < 2:
            errors['1'] = " username  name  is too short"
                
       # Name regex to check for name shoud not contain any number

        if not NAME_REGEX.match(postData['name']):  
            errors['2'] = "Name shoud contain only letter and at least 2 character"

        if not NAME_REGEX.match(postData['username']):
            errors['2'] = "Name shoud contain only letter and at least 2 character"
            
            
        #Email check and its uniqueness!

        if not EMAIL_REGEX.match(postData['email']):
            errors['3'] = "Invalid email!"

        #Checking email is exist
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['4'] = "Email is already exist!"

        # Birthday
        try:
            dob = datetime.datetime.strptime(postData['birth_day'], '%Y-%m-%d')
            if dob > datetime.datetime.now():
                errors['bday'] = "Birhday day shoud be valid !"
 
        except:
            errors['bday'] = "You did not enter a birthday"

         #password check for length and Regex

        if len(postData['password']) <=8:
            errors['psw'] = "password  should be more than 8 characters"
        
        if len(postData['cnf']) <=8:
            errors['pswc'] = " password is required!"
            
        if postData['password'] != postData['cnf']:
            errors['pswcc'] = "Password shoud match!"

        if not PASS_REGEX.match(postData['password']):
            errors['pswrg'] = "password shoud be 8 char min with one upper case lower case one special char"

        if len(errors) > 0:
            return errors       

                       
        hashme = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        
        my_user = User.objects.create(
            name=postData['name'],
            username =postData['username'],
            email=postData['email'],
            birth_day=postData['birth_day'],
            gender = postData['Gender'],                
            password=hashme
        )
        my_user.save()

        return errors

    def login_valiator(self, postData):
        errors = {}

        logchk = User.objects.filter(email=postData['email'])
        if logchk:
            psk = logchk.values()[0]['password']
            if not bcrypt.checkpw(postData['password'].encode(),logchk.values()[0]['password'].encode()):
                errors['password'] = "Email and password is Invalid!"
       
        else:
            errors['password'] = "Email and password is Invalid!"

        return errors

    

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=100)  
    password = models.CharField(max_length=16)
    birth_day = models.DateTimeField(default=None )  
    gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)    
     
    objects = UserManager()

class Trip(models.Model):    
    destination = models.CharField(max_length=255)
    start_date = models.CharField(max_length=45)
    end_date = models.CharField(max_length=45)
    plan = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Group(models.Model):    
    guest = models.ForeignKey(User)
    trip = models.ForeignKey(Trip)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)