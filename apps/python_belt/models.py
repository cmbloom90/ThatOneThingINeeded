# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def register(self, name, username, email, password, confirm, start):
        errors = []
        if len(name) < 2:
            errors.append("Name must be 2 characters or more")

        if len(username) < 2:
            errors.append("Username must be 2 characters or more")

        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) > 0:
                errors.append("Email already in use")


        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        if len(confirm) < 1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        if len(start)<1:
            errors.append("Hire Date must be entered!")
        else:
            st = datetime.strptime(start, "%Y-%m-%d")
            print st             
            if st>datetime.now():
                errors.append("Hire Date must be in the past")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            response["user"] = User.objects.create(
                name=name,
                username=username,
                email=email.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                start=start
            )

        return response

    def login(self, username, password):
        errors = []

        if len(username) < 1:
            errors.append("Username is required")
        else:
            usersName = User.objects.filter(username=username)
            if len(usersName) == 0:
                errors.append("Username does not match")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) == 0:
            if bcrypt.checkpw(password.encode(), usersName[0].password.encode()):
                response["user"] = usersName[0]
            else:
                errors.append("Incorrect password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response

class ItemManager(models.Manager):
    def addItem(self, name, user_id):
        errors=[]
        if len(name)<1:
            errors.append("The Item must be entered!")
        if len(name)< 3:
            errors.append("Item name must be more than 3 characters")

        if len(errors)>0:
            return {"valid":False, "errors":errors}
        else:
            Item.objects.create(
                name=name,
                user_id=user_id
            ).item_user.add(User.objects.get(id=user_id))
            return {"valid":True, "errors":errors}


class User(models.Model):
    name = models.CharField(max_length=255) 
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start = models.DateField()
    objects = UserManager()

    def __repr__(self):
        return "Users Object({}) {} {}>".format(self.id, self.name, self.username)  

class Item(models.Model):
    name= models.CharField(max_length= 255)
    user= models.ForeignKey(User,on_delete=models.CASCADE, related_name= "adder") 
    item_user= models.ManyToManyField(User, related_name="user_item") 
    created_at=models.DateTimeField(auto_now_add=True) 
    objects=ItemManager()
