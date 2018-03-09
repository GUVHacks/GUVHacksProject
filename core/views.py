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


def register(request):

	user_form = UserForm()
	context = {'user_form': user_form}

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'],
											email=form.cleaned_data['email'],
											password=form.cleaned_data['password'])
			messages.add_message(request, messages.SUCCESS, 'Account created.')
			return redirect('login')
		else:
			messages.add_message(request, messages.ERROR, 'Invalid form.')

	return render(request, 'core/register.html', context)


def login(request):
	
	login_form = LoginForm()
	context = {'login_form': login_form}

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			#user = authenticate(username=form.cleaned_data.get('username'), 
			#					password=form.cleaned_data.get('password'))
			user = authenticate(username=request.POST.get('username'), 
									password=request.POST.get('password'))

			if user is not None:
				auth_login(request, user)
				if not Account.objects.filter(user=request.user).exists():
					return redirect('account-setup')
				else:
					return redirect('/login/')
			else:
				messages.add_message(request, messages.ERROR, 'Invalid login credentials.')
				return redirect('/login/')
		else:
			print(form.errors)
			messages.add_message(request, messages.ERROR, 'Invalid form')
			return redirect('/login/')

	return render(request, 'core/login.html', context)


@login_required(login_url='login')
def account_setup(request):

	account_form = AccountForm()
	context = {'account_form': account_form}

	if request.method == 'POST':
		form = AccountForm(request.POST)
		if form.is_valid():
			account = form.save(commit=False)
			account.user = request.user
			account.save()
			return redirect('history')
		else:
			print(form.errors)
			messages.add_message(request, messages.ERROR, 'Invalid form')			

	return render(request, 'core/account-setup.html', context)


@login_required(login_url='login')
def history(request):
	employment_form = EmploymentForm()
	prev_employment = Employment.objects.filter(account=request.user.account)

	context = {'employment_form': employment_form,
			   'employment': prev_employment}

	if request.method == 'POST':
		action = request.POST.get('action')
		print(action)
		if action == 'add_employment':
			form = EmploymentForm(request.POST)
			if form.is_valid():
				employment = form.save(commit=False)
				employment.account = request.user.account
				employment.save()
				messages.add_message(request, messages.SUCCESS, 'Employment Added')
			else:
				print(form.errors)
				messages.add_message(request, messages.ERROR, 'Invalid form')

	return render(request, 'core/history.html', context)


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully.')
    return redirect('/')