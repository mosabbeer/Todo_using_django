from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from todo_project import models
from todo_project.models import todo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password =request.POST.get('pass')
        print(username,email,password)
        my_user=User.objects.create_user(username,email,password)
        my_user.save()
        return redirect('/login')
    return render(request,'signup.html')
def login_view(request):
    if request.method=='POST':
        usernam=request.POST.get('username')
        passwor=request.POST.get('pass')
        print(usernam,passwor)
        user=authenticate(request,username=usernam,password=passwor)
        if user is not None:
            login(request,user)
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request,'login.html')
def todo_view(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj=models.todo(title=title,user=request.user)
        obj.save()
        res = models.todo.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage',{'res':res})
    res = models.todo.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html',{'res':res})
def index(request):
    return render(request,'index.html')
def edit_todo(request, srno):
    obj=models.todo.objects.get(srno=srno)
    if request.method=='POST':
        title=request.POST.get('title')
        obj.title=title
        obj.save() 
        return redirect('/todopage')
    return render(request,'todo_edit.html',{'todo':obj})
def delete_todo(request,srno):
    obj=models.todo.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')
def signout(request):
    logout(request)
    return redirect('/login')