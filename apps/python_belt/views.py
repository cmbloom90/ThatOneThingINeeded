# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


# Create your views here.
def index(request):

	return render(request, "python_belt/index.html")

def register(request):
	check = User.objects.register(
		request.POST["name"],
		request.POST["username"],
		request.POST["email"],
		request.POST["password"],
		request.POST["confirm"],
		request.POST["start"]
	)

	if not check["valid"]:
		for error in check["errors"]:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")
	else:
		request.session["user_id"] = check["user"].id
		
		return redirect("/dashboard")

	

def login(request):
	
	check = User.objects.login(
        request.POST["username"],
        request.POST["password"]
    )

	if not check["valid"]:
		for error in check["errors"]:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")
	else:
		request.session["user_id"] = check["user"].id
		
		return redirect("/dashboard")

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "See you later")
    return redirect("/")	

def dashboard(request):
	if "user_id" not in request.session:
    		messages.add_message(request, messages.ERROR, "You need to log in first")
        	return redirect("/")
	user = User.objects.get(id=request.session["user_id"])
	user_items=User.objects.get(id=request.session["user_id"]).user_item.all()
	other_items= Item.objects.all().exclude(item_user=request.session["user_id"])    	
	data={
		"user": user,
		"user_items": user_items,
		"other_items":other_items[:10],
	}
	return render(request, "python_belt/dashboard.html", data) 

def create(request):
	if "user_id" not in request.session:
	    messages.add_message(request, messages.ERROR, "You need to log in first")
	    return redirect("/")
	return render(request, "python_belt/create.html")

def create_item(request):
	if "user_id" not in request.session:
		messages.add_message(request, messages.ERROR, "You need to log in first")
		return redirect("/")
	check= Item.objects.addItem(
		request.POST["name"],
		request.session["user_id"]
	)
	if not check["valid"]:
		for error in check ["errors"]:messages.add_message(request, messages.ERROR, error)
		return redirect("/wish_items/create")
	else:
		return redirect("/dashboard")	

def item(request, item_id):
	if "user_id" not in request.session:
		messages.add_message(request, messages.ERROR, "You need to log in first")
		return redirect("/")

	item= Item.objects.get(id=item_id)
	added_by=User.objects.get(adder=item_id).id
	other_wishers= User.objects.filter(user_item=item.id)

	data={
		"item":item,
		"added_by":added_by,
		"other_wishers":other_wishers
	}	

	return render(request, "python_belt/item.html", data)


def add(request, item_id):
	if "user_id" not in request.session:
	    messages.add_message(request, messages.ERROR, "You need to log in first")
	    return redirect("/")

	user= User.objects.get(id=request.session["user_id"])
	item= Item.objects.get(id= item_id)
	item.item_user.add(user)

	return redirect("/dashboard")    

def remove(request, item_id):
	if "user_id" not in request.session:
	    messages.add_message(request, messages.ERROR, "You need to log in first")
	    return redirect("/")

	user= User.objects.get(id=request.session["user_id"]).id
	item= Item.objects.get(id= item_id)
	added_by=User.objects.get(adder=item_id).id

	if user == added_by:
		item.delete()
		messages.add_message(request, messages.ERROR,"The item was Deleted.")
		print True
	else:
		item.item_user.remove(user)
		messages.add_message(request, messages.ERROR,"The item was removed from your Wish List.")
		print False	
	return redirect('/dashboard')	
