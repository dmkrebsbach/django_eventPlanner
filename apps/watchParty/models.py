from django.db import models
from validate_email import validate_email   ## validating email the long way (use type="email")
import bcrypt                               ## for hashing, encrypting passwords
import datetime                             ## birthdate validation
import re                                   ## this is for password matching

class userManager(models.Manager):
    def registrationValidator(self, userData):
        errors = {}

        ## First Name Validation ##
        if len(userData['firstName']) < 2:
            errors['firstName'] = "First Name must be at least two [2] characters"
        if not userData['firstName'].isalpha():
            errors['firstName'] = "First Name must contain letters only (no numbers, special characters OR spaces)"

        ## Last Name Validation ##
        if len(userData['lastName']) < 2:
            errors['lastName'] = "Last Name must be at least two [2] characters"
        if not userData['lastName'].isalpha():
            errors['lastName'] = "Last Name must contain letters only (no numbers, special characters OR spaces)"

       # Email Validation -- if input type = "email" on HTML, there is no need to validate the format as an email address ##
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(userData['email']):
            errors['email'] = "Email must be in valid format"
        if User.objects.filter(email = userData["email"]):
            errors['email'] = "This Email Address is already Registered; please Login or use another Email Address"

        # #birthDate (13 Years Old Minimum)
        # cutoff = datetime.datetime.now() - datetime.timedelta(days = (13 * 365)+12/4)
        # date = datetime.datetime.strptime(userData["birthDate"], "%Y-%m-%d")
        # if date > cutoff:
        #     errors["birthday"] = "Must be at least 13 years old to access this website."

        # # Alias / Username Validation
        # if User.objects.filter(alias = userData["alias"]):
        #     errors['alias'] = "This Alias is already Registered; please use another Alias"

        ## Password Validation ##
        if len(userData['password']) < 8:
            errors['password'] = "Password must be at least eight [8] characters"
        
        # if not re.match('.*[0-9]', userData['password']):
        #     errors['password'] = "Password must include at least one [1] number between [0-9]"
        
        # if userData["password"] != userData["confirmPass"]:
        #     errors["password"] = "Passwords do not match; please try again"

        # ## validation for special characters in password ##
        # specialCharacters = ['!', '@', '#', '$', '%', '^', '&', '*']
        # password = userData["password"]
        # if not any (c in specialCharacters for c in password):
        #     errors["password"] = "Password does not contain at least one special character (!,@,#,$,%,^,&, or *)"

        return errors

    def loginValidator(self, userData):
        errors = {}

        try:
            user = User.objects.get(email = userData["loginEmail"])

        except:
            errors["loginEmail"] = f"No email address matching {userData['loginEmail']} or "
            errors["loginEmail2"] = "an account associated with this email does not exist"
            return errors
        
        if not bcrypt.checkpw(userData["password"].encode(), user.password.encode()):
            errors["password"] = "Password does not match email address associated with this account. Please try again."

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    objects = userManager()

class Event(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    eventDate = models.DateField()
    location = models.CharField(max_length=255)
    attendees = models.ManyToManyField(User, related_name="events")
    host = models.ForeignKey(User, related_name="hosting")


