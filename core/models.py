# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

COUNTRIES = (('Italy', 'Italy'),
			 ('France', 'France'),
			 ('Germany', 'Germany')
			)

REASONS = (('health', 'Health'),
			 ('lost_job', 'Lost Job'),
			 ('migration_issues', 'Migration Issues'),
			 ('other', 'Other')
			)

class Account(models.Model):
	# Link to the Django user account
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	name = models.CharField(max_length=256)
	phone = models.CharField(max_length=100) # function to verify real phone number in form?
	address = models.CharField(max_length=256) # change to multiple lines, etc?
	city = models.CharField(max_length=256)
	gender = models.BooleanField(default=False) # male is false, female is true
	age = models.IntegerField()
	country = models.CharField(max_length=256, choices=COUNTRIES)
	profile_photo = models.FileField(null=True, upload_to="profile_photos/")
	credit_score = models.IntegerField(blank=True, null=True)

	has_lease = models.BooleanField(default=False)


class Employment(models.Model):
	account = models.ForeignKey(Account)
	employer = models.CharField(max_length=256)
	paystub = models.FileField(blank=True, null=True, upload_to="paystubs/")
	phone = models.CharField(max_length=100) # function to verify real phone number in form?
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True)
	currently_employed = models.BooleanField(default=False, verbose_name="Currently Employed")
	monthly_salary = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Monthly Salary")


class Identification(models.Model):
	account = models.OneToOneField(Account)
	name = models.CharField(max_length=100)
	file = models.FileField(upload_to='id_documents/')


class FinancialInfo(models.Model):
	account = models.OneToOneField(Account)

	monthly_income = models.DecimalField(decimal_places=2, max_digits=12, default=0)
	housing_expense = models.DecimalField(decimal_places=2, max_digits=12, default=0)
	
	time_in_europe = models.IntegerField() # in months
	
	has_bank_account = models.BooleanField(default=False)
	amount_in_bank = models.DecimalField(decimal_places=2, max_digits=12, default=0)
	amount_cash = models.DecimalField(decimal_places=2, max_digits=12,blank=True, null=True)

	has_debts = models.BooleanField(default=False)
	amount_debts = models.DecimalField(decimal_places=2, max_digits=12, blank=True, default=0)
	num_months_debt = models.IntegerField(blank=True, null=True, default=0)
	ongoing_debt = models.BooleanField(default=False)
	reason_ongoing = models.CharField(max_length=256, choices=REASONS, blank=True, null=True)

	# What more needs to go here?
	missed_payments = models.IntegerField(blank=True, null=True, default=0)

	loan_file = models.FileField(upload_to="loan_docs/", blank=True, null=True)


class Group(models.Model):
	name = models.CharField(max_length=256)
	code = models.CharField(max_length=256)


class Lease(models.Model):
	account = models.OneToOneField(Account)

	amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
	leaser_name = models.CharField(max_length=256)
	leaser_email = models.CharField(max_length=256)

	guarantor_name = models.CharField(max_length=256)
	gurantor_email = models.CharField(max_length=256)

	group = models.ForeignKey(Group)


