# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.forms import *
from core.models import *

@login_required(login_url='/login/')
def index(request):

	context = {'message': "hello"}
	
	return render(request, 'core/index.html', context)


def login(request):
	
	login_form = LoginForm()
	context = {'login_form': login_form}

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data.get('username'), 
								password=form.cleaned_data.get('password'))
			if user is not None:
				auth_login(request, user)
				return redirect('/')
			else:
				messages.add_message(request, messages.ERROR, 'Invalid login credentials.')
				return redirect('/login/')
		else:
			print(form.errors)
			messages.add_message(request, messages.ERROR, 'Invalid form')
			return redirect('/login/')

	return render(request, 'core/login.html', context)


def register(request):

	user_form = UserForm()
	context = {'user_form': user_form}

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			# Create the linked account model
			messages.add_message(request, messages.SUCCESS, 'Account created.')
			redirect('/login/')
		else:
			messages.add_message(request, messages.ERROR, 'Invalid form.')



	return render(request, 'core/register.html', context)


def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully.')
    return redirect('/')