# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
	# Link to the Django user account
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	name = models.CharField(max_length=256)
	phone = models.CharField(max_length=100) # function to verify real phone number in form?
	address = models.CharField(max_length=256) # change to multiple lines, etc?
	city = models.CharField(max_length=256)
	gender = models.BooleanField(default=False) # male is false, female is true
	age = models.IntegerField()
	profile_photo = models.FileField(null=True, upload_to="profile_photos/")


class Employment(models.Model):
	account = models.ForeignKey(Account)
	employer = models.CharField(max_length=256)
	paystub = models.FileField(null=True, upload_to="paystubs/")
	phone = models.CharField(max_length=100) # function to verify real phone number in form?
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True)
	currently_employed = models.BooleanField(default=False, verbose_name="Currently Employed")
	wage = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Hourly Wage")


class Identification(models.Model):
	account = models.ForeignKey(Account)
	name = models.CharField(max_length=100)
	file = models.FileField(upload_to='id_documents/')


class FinancialInfo(models.Model):
	monthly_income = models.DecimalField(decimal_places=2, max_digits=12)
	housing_expense = models.DecimalField(decimal_places=2, max_digits=12)
	
	time_in_europe = models.IntegerField() # in months
	
	has_bank_account = models.BooleanField(default=False)
	amount_in_bank = models.DecimalField(decimal_places=2, max_digits=12)

	has_cash = models.BooleanField(default=False)
	amount_cash = models.DecimalField(decimal_places=2, max_digits=12)

	has_debts = models.BooleanField(default=False)
	amount_debts = models.DecimalField(decimal_places=2, max_digits=12)

	# What more needs to go here?
	missed_payments = models.IntegerField()



