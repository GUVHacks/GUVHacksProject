# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from .creditScore import creditScore
from django.core.mail import send_mail

from core.forms import *
from core.models import *

@login_required(login_url='/login/')
def index(request):

	context = {'user': request.user,
			   'credit_score': request.user.account.credit_score}
	
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
					return redirect('/')
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
		form = AccountForm(request.POST, request.FILES)
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
	file_form = IdentificationForm()
	# prefill if it already exists, and dont create a new one
	fin_info_form = FinancialInfoForm()

	context = {'employment_form': employment_form,
			   'employment': prev_employment,
			   'file_form': file_form,
			   'user': request.user,
			   'fin_info_form': fin_info_form}

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
		elif action == 'add_id':
			form = IdentificationForm(request.POST, request.FILES)
			if form.is_valid():
				identification = form.save(commit=False)
				identification.account = request.user.account
				identification.save()
				messages.add_message(request, messages.SUCCESS, 'ID Added')
			else:
				print(form.errors)
		elif action == 'fin_info':
			form = FinancialInfoForm(request.POST)
			if form.is_valid():
				fin_info = form.save(commit=False)
				fin_info.account = request.user.account
				fin_info.save()
				messages.add_message(request, messages.SUCCESS, 'Information saved.')
				credit_score = getUpdatedCreditScore(request)
				print(credit_score)
				account.credit_score = credit_score
				account.save()
			else:
				print(form.errors)

	return render(request, 'core/history.html', context)


@login_required(login_url='login')
def profile(request):

	profile = request.user.account
	url = "guvhacks/media/"

	context = {'profile': profile,
			   'url': url}
	return render(request, 'core/profile.html', context)


class EditPersonalInfoView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = "core/edit-profile.html"

    def get_object(self, *args, **kwargs):
        user = self.request.user

        return user.account

    def get_success_url(self, *args, **kwargs):
        return reverse('profile')



@login_required(login_url='login')
def financials(request):

	employment_form = EmploymentForm()
	financials = FinancialInfo.objects.get(account=request.user.account)
	account = request.user.account
	context = {'account': account,
			   'financials': financials,
			   'employment_form': employment_form}


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
		elif action == 'delete_employment':
			pk = request.POST.get('pk')
			employment = Employment.objects.get(pk=pk)
			employment.delete()

	return render(request, 'core/financials.html', context)


class EditFinancialInfoView(UpdateView):
    model = FinancialInfo
    form_class = FinancialInfoForm
    template_name = "core/edit-financials.html"

    def get_object(self, *args, **kwargs):
        user = self.request.user
        financials = FinancialInfo.objects.get(account=user.account)

        return financials

    def get_success_url(self, *args, **kwargs):
        return reverse('financials')


@login_required(login_url='login')
def faq(request):
	context = {}
	return render(request, 'core/faq.html', context)


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully.')
    return redirect('/')

#Param list:
#country: string: "Italy" or "Germany" or "France"
#curIncMo: int or float: current monthly income if user input is hourly wage, 
#            curIncMo = 200*wage (consider working 200 hours per month)
#workExp: boolean. If user has work experience: True, else: False
#bankAcc: Boolean. If user has bank account: True, else: False
#bankBal: int or float: user's bank account balance
#cashBal: int or float: user's cash available for purchase
#arrLenMo: int: months that the user has been to Europe
#outDebt: Boolean: if the user has outstanding debt/loan from bank or NGO: True
#outDebtAmt: int or float: amount of the debt 
#outDebtTerm: int: number of months for the debt
#paidDebt: Boolean: if the user has been issued loan and the loan has been fully repaid
#misPay: Boolean: if the user has any missed payment in the past 2 years 
#misPayFreq: int: total frequencies the user missed a payment in the past 2 years 
 


