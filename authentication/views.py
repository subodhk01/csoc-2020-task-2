from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User


def loginView(request):
    if request.user.is_authenticated :
        return redirect('index')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', { 'msg': "Invalid Credentials" })
    else:
        return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return redirect('index')

def registerView(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
        except:
            return render(request, 'signup.html', { 'msg': "Missing fields" })
        if password1 != password2:
            return render(request, 'signup.html', { 'msg': "Passwords not matching" })
        try:
            user = User.objects.create_user(
                username = username,
                first_name = firstname,
                last_name = lastname,
                email = email,
                password = password1
            )
            user.save()
        except:
            return render(request, 'signup.html', { 'msg': "Username already exists" })
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'signup.html', { 'msg': "User created Successfully" })
    else:
        return render(request, 'signup.html')
