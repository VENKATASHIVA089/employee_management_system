from django.shortcuts import render, get_object_or_404,redirect
#from django.http import HttpResponceRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from employee.forms import UserForm

# Create your views here.
def user_login(request):
	context={}
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username,password=password)
		if user:
			login(request,user)
			if request.GET.get('next',None):
				return redirect(request.GET['next'])
			return redirect('employee_list')
		else:
			context['error']='Enter valid credentials !!'
			return render(request,'auth/login.html',context)
	else:
		return render(request,'auth/login.html',context)
def user_logout(request):
	if request.method=='POST':
		logout(request)
		return redirect('user_login')
@login_required(login_url='/login/')
def success(request):
	context={}
	context['user']=request.user
	return render(request,'auth/success.html',context)


@login_required(login_url='/login/')
def employee_list(request):
	context={}
	context['users']=User.objects.all()
	context['title']='Employees'
	return render(request,'employee/index.html',context)

@login_required(login_url='/login/')
def employee_details(request,id=None):
	context={}
	context['user']=get_object_or_404(User,id=id)
	return render(request,'employee/details.html',context)

@login_required(login_url='/login/')
def employee_add(request):
	context={}
	if request.method=='POST':
		user_form=UserForm(request.POST)
		context['user_form']=user_form
		if user_form.is_valid():
			user_form.save()
			return redirect('employee_list')
		else:
			return render(request,'employee/add.html',context)
	else:
		user_form=UserForm()
		context['user_form']=user_form
		return render(request,'employee/add.html',context)

@login_required(login_url='/login/')
def employee_edit(request,id=None):
	user=get_object_or_404(User,id=id)
	context={}
	if request.method=='POST':
		user_form=UserForm(request.POST,instance=user)
		context['user_form']=user_form
		if user_form.is_valid():
			user_form.save()
			return redirect('employee_list')
		else:
			return render(request,'employee/edit.html',context)
	else:
		user_form=UserForm(instance=user)
		context['user_form']=user_form
		return render(request,'employee/edit.html',context)
@login_required(login_url='/login/')
def employee_delete(request,id=id):
	user=get_object_or_404(User,id=id)
	if request.method=='POST':
		user.delete()
		return redirect('employee_list')
	else:
		context={
			'user':user
		}
		return render(request,'employee/delete.html',context)
	