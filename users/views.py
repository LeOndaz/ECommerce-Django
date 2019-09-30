from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse, reverse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout


class RegisterView(View):
	def post(self, *args, **kwargs):
		print(self.request.POST)
		form = RegisterForm(self.request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			pwd = make_password(form.cleaned_data['password'])
			User.objects.create(username=username, email=email, password=pwd).save()
			messages.info(self.request, 'Account created succesfully, You may log in')
			return redirect('/')


class MainLoginView(LoginView):
	def post(self, *args, **kwargs):
		user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
		if user is not None:
			login(self.request, user)
			return redirect('/')
		else:
			messages.error(self.request, 'Invalid info')
			return redirect('/')


class MainLogoutView(LogoutView):
	def get(self, *args, **kwargs):
		logout(self.request)
		messages.info(self.request, "You've been logged out successfuly, Let us see you again soon!")
		return redirect('/')
